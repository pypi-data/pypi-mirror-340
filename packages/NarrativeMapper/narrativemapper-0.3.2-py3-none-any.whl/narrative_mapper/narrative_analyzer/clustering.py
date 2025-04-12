from sklearn.metrics.pairwise import pairwise_distances, cosine_distances
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from .utils import progress_bars
from math import sqrt, log2
import umap.umap_ as umap
import hdbscan
import pandas as pd
import numpy as np
import warnings

def get_param_calcs(df, umap_kwargs=None, hdbscan_kwargs=None, verbose=False):
    '''
    Autocalculates some UMAP and HDBSCAN parameters based on dataset size.

    Parameters autocalculated:
        HDBSCAN: min_cluster_size, min_samples
        UMAP: n_components, n_neighbors
    '''
    text_list = df['text'].tolist()
    num_texts = len(text_list)
    base_num_texts = 500
    N = max(1, num_texts / base_num_texts)

    if "n_components" not in umap_kwargs: 
        #n_components ~ constant to N. 
        n_components = 10
        umap_kwargs['n_components'] = n_components

    if "n_neighbors" not in umap_kwargs:
        #n_neighbors ~ cube root of N. range [15, 75]
        n_neighbors = int(min(75, max(15, 15*(N**(1/3)))))
        umap_kwargs['n_neighbors'] = n_neighbors

    if "min_cluster_size" not in hdbscan_kwargs:
        #min_cluster_size ~ sqrt(N). range [25, 200]
        min_cluster_size = int(min(200, max(25, 25*sqrt(N))))
        hdbscan_kwargs['min_cluster_size'] = min_cluster_size

    if "min_samples" not in hdbscan_kwargs:
        #min_samples ~ log2(N). range [5, 30]
        min_samples = int(min(30, max(5, 5*log2(N))))
        hdbscan_kwargs['min_samples'] = min_samples

    if verbose:
        print(f"[CLUSTERING PARAMS]")
        print(f"Text count: {num_texts}")
        print(f"UMAP n_components: {umap_kwargs['n_components']}")
        print(f"UMAP n_neighbors: {umap_kwargs['n_neighbors']}")
        print(f"HDBSCAN min_cluster_size: {hdbscan_kwargs['min_cluster_size']}")
        print(f"HDBSCAN min_samples: {hdbscan_kwargs['min_samples']}")

def merge_clusters_union_find(df, threshold=0.2, embedding_col='embeddings', cluster_col='cluster'):
    '''
    Union Find algorithm to merge alike clusters. The algorithm requires state to be held, so
    using a class makes it cleaner.
    '''
    class UnionFind:
        def __init__(self, items):
            #each item is its own parent initially
            self.parent = {item: item for item in items}
        
        def find(self, x):
            #path compression
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        
        def union(self, x, y):
            rootX = self.find(x)
            rootY = self.find(y)
            if rootX != rootY:
                #attach one's root to the other's root
                self.parent[rootY] = rootX
        
    #compute centroids
    centroids = {}
    for c_id in df[cluster_col].unique():
        emb = np.vstack(df.loc[df[cluster_col] == c_id, embedding_col])
        centroids[c_id] = emb.mean(axis=0)
    
    #compute pairwise distances
    ids = list(centroids.keys())
    vectors = [centroids[cid] for cid in ids]
    dists = cosine_distances(vectors)
    
    #initialize Union-Find structure
    uf = UnionFind(ids)
    
    #for each close pair, union them
    n = len(ids)
    for i in range(n):
        for j in range(i+1, n):
            if dists[i, j] < threshold:
                uf.union(ids[i], ids[j])
    
    #reassign cluster IDs based on the union-find root
    new_labels = {}
    for c_id in ids:
        new_labels[c_id] = uf.find(c_id)
    
    df[cluster_col] = [new_labels[c] for c in df[cluster_col]]
    return df

def cluster_embeddings(
    df, 
    verbose=False,
    umap_kwargs=None,
    hdbscan_kwargs=None,
    pca_kwargs=None,
    use_pca=True
    ) -> pd.DataFrame:
    """
    Preprocesses using L2 normalization and PCA.

    Reduces dimensionality of embedding vectors using UMAP and clusters them using HDBSCAN.

    Each DataFrame must include an 'embedding_vector' col. After clustering, a 'cluster' label is added
    to each DataFrame. The function returns a DataFrame with all original cols
    and the assigned 'cluster' label, excluding the noise cluster (cluster = -1).

    Parameters:
        df (DataFrame): DataFrame with embeddings column.
        verbose (bool): Shows progress timer if true.
        umap_kwargs (dict): Allows for more UMAP input parameters
        hdbscan_kwargs (dict): Allows for more HDBSCAN input parameters
        pca_kwargs (dict): Allows for more PCA input parameters
        use_pca (bool): Allows user to not use PCA and go straight to UMAP

    Returns:
        DataFrame: DataFrame of clustered items with a 'cluster' column.
    """
    
    embeddings = np.array(df['embeddings'].tolist(), dtype=np.float32) #convert to np.array with float32 vals for less mem usage

    #set base params
    if umap_kwargs == None: umap_kwargs={'min_dist': 0.0, 'random_state': 42, 'metric': 'euclidean'}
    if hdbscan_kwargs == None: hdbscan_kwargs={'metric': 'euclidean'}
    if pca_kwargs == None: pca_kwargs={'n_components': 100, 'random_state': 42}

    #these variables are used for error testing
    umap_metric = umap_kwargs.get('metric', 'euclidean') #since UMAP default sets euclidean
    hdbscan_metric = hdbscan_kwargs.get('metric', 'euclidean') #since HDBSCAN default sets euclidean

    #autocalculate some import UMAP and HDBSCAN parameters
    get_param_calcs(df, umap_kwargs=umap_kwargs, hdbscan_kwargs=hdbscan_kwargs, verbose=verbose)

    #'rich' progress bar
    progress_context = progress_bars(verbose, bars=False)

    with progress_context as progress:
        if verbose:
            task = progress.add_task("[cyan]Clustering...", total=1)
        
        if hdbscan_metric == 'cosine':
            raise ValueError("HDBSCAN does not support cosine.")

        if umap_metric != hdbscan_metric:
            raise ValueError("UMAP and HDBSCAN must use the same distance metric.")

        if hdbscan_metric != 'euclidean': #PCA and L2 are preprocessing steps for euclidean
            warnings.warn(f"PCA and L2 Normalization not supported for metric '{hdbscan_kwargs['metric']}'. Skipping both.")
        
        else:
            embeddings = normalize(embeddings, norm='l2') #since both UMAP + HDBSCAN are setup for euclidean
            if use_pca:
                try:
                    pca = PCA(**pca_kwargs)
                    embeddings = pca.fit_transform(embeddings) #returns float32 when float32 is input

                except Exception as e:
                    raise RuntimeError(f"Error during PCA") from e

        #UMAP dimensionality:
        try:
            warnings.filterwarnings("ignore", message=".*n_jobs value 1 overridden.*")
            umap_reducer = umap.UMAP(
                **umap_kwargs       
            )
            embeddings = umap_reducer.fit_transform(embeddings)

        except Exception as e:
            raise RuntimeError(f"Error during UMAP") from e

        #HDBSCAN clustering:
        try:
            clusterer = hdbscan.HDBSCAN(
                **hdbscan_kwargs
            )
            cluster_labels = clusterer.fit_predict(embeddings)

        except Exception as e:
            raise RuntimeError(f"Error during HDBSCAN") from e

        if verbose:
            progress.update(task, advance=1)

    df = df.copy() #may not need this
    df['cluster'] = cluster_labels.tolist()
    df = df[df['cluster'] != -1] #drop noise cluster

    if verbose:
        num_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
        print(f"HDBSCAN found {num_clusters} clusters.")

    merged_df = merge_clusters_union_find(df, threshold=0.3)  #similarity cutoff 

    if verbose:
        num_clusters = len(set(merged_df))
        print(f"{num_clusters} clusters after merging.")
    
    return merged_df