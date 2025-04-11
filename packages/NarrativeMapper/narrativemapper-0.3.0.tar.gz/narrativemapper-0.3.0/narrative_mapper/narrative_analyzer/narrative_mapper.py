from .embeddings import get_embeddings
from .clustering import cluster_embeddings
from .summarize import summarize_clusters
from .formatters import format_by_text, format_by_cluster, format_to_dict
import pandas as pd

class NarrativeMapper:
    """
    A pipeline for processing, clustering, summarizing, and formatting text data.

    Methods allow you to load embeddings from a file, perform clustering,
    generate cluster summaries, and format the results into various output structures.
    """
    
    def __init__(self, df, online_group_name: str, verbose=False):
        """
        Initializes the NarrativeMapper instance.
        
        Parameters:
            online_group_name (str): Name of the online community (e.g. subreddit) to label outputs.
            df (DataFrame): The DataFrame of the original file.
            verbose (bool): Shows all progress bars and timers for all parts of the pipeline.
            embeddings_df (DataFrame): Contains DataFrame after embeddings.
            cluster_df (DataFrame): Contains DataFrame after clustering.
            summary_df (DataFrame): Contains DataFrame after summarizing.
        """
        self.file_df = df
        self.online_group_name = online_group_name
        self.verbose = verbose
        self.embeddings_df = None
        self.cluster_df = None
        self.summary_df = None

    def load_embeddings(self) -> "NarrativeMapper":
        """
        Loads and processes text data to obtain OpenAI embeddings.
        
        Parameters:
            batch_size (int): length of text-list chunks being send to OpenAI embeddings
        
        Returns:
            NarrativeMapper: Self, with embeddings loaded.
        """
        self.embeddings_df = get_embeddings(self.file_df, self.verbose)
        return self

    def cluster(
        self,
        umap_kwargs={'n_components': 10, 'n_neighbors': 20},
        hdbscan_kwargs={'min_cluster_size': 30, 'min_samples': 10},
        pca_kwargs={'n_components': 100},
        use_pca=True
        ) -> "NarrativeMapper":
        """
        Applies PCA + UMAP for dimensionality reduction and HDBSCAN for clustering
        on the loaded embeddings.
        
        Parameters:
            umap_kwargs (dict): Allows for more UMAP input parameters
            hdbscan_kwargs (dict): Allows for more HDBSCAN input parameters
            pca_kwargs (dict): Allows for more PCA input parameters
            use_pca (bool): Allows user to not use PCA and go straight to UMAP
        
        Returns:
            NarrativeMapper: Self, with clustering results stored.
        """
        self.cluster_df = cluster_embeddings(
            self.embeddings_df,
            verbose=self.verbose,
            umap_kwargs=umap_kwargs,
            hdbscan_kwargs=hdbscan_kwargs,
            pca_kwargs=pca_kwargs,
            use_pca=use_pca
        )
        return self

    def summarize(self, max_sample_size: int=500) -> "NarrativeMapper":
        """
        Summarizes each cluster using GPT-based keyword extraction and sentiment analysis.

        Parameters:
            max_sample_size (int): max length of text list for each cluster being sampled
        
        Returns:
            NarrativeMapper: Self, with summarized clusters stored.
        """
        self.summary_df = summarize_clusters(self.cluster_df, max_sample_size, verbose=self.verbose)
        return self

    def format_by_text(self) -> pd.DataFrame:
        """
        Returns a DataFrame where each row represents an individual comment with its sentiment.
        
        Returns:
            pd.DataFrame: Text-level formatted output.
        """
        return format_by_text(self.summary_df, self.online_group_name)

    def format_by_cluster(self) -> pd.DataFrame:
        """
        Returns a DataFrame summarizing clusters with overall sentiment and comment counts.
        
        Returns:
            pd.DataFrame: Cluster-level formatted output.
        """
        return format_by_cluster(self.summary_df, self.online_group_name)

    def format_to_dict(self) -> dict:
        """
        Returns the summarized clusters in a dictionary format.
        
        Returns:
            dict: A dictionary with cluster summaries, suitable for JSON export.
        """
        return format_to_dict(self.summary_df, self.online_group_name)
