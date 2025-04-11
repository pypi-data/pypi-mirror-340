from captum.attr import DeepLift
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logomaker
import warnings
import pickle
from pathlib import Path
import os

from utils.motif_utils import (
    find_most_significant_kmer_in_sequence,
    one_hot_to_DNA,
    pairwise_distance,
    tsne_kmeans_search_silhouette,
    create_pwm_for_cluster,
    convolve_pwm_with_sequences,
    perform_chi_squared_tests,
    representation,
)

warnings.filterwarnings("ignore")


class CluMo:
    """
    CluMo (Clustering Motifs) is a tool for DNA motif discovery using deep learning models.

    It takes a trained PyTorch model and DNA sequences as input, and identifies
    statistically significant motifs using feature attribution and clustering.
    """

    def __init__(self, model=None, output_dir="motifs", name="clumo_run"):
        """
        Initialize CluMo for motif discovery.

        Parameters:
        -----------
        model : torch.nn.Module, optional
            A trained PyTorch model for feature attribution
        model_path : str, optional
            Path to a saved PyTorch model file (.pt)
        output_dir : str, default="motifs"
            Directory to save discovered motifs
        name : str, default="clumo_run"
            Name for this analysis run
        """
        if model is None:
            raise ValueError("a torch model must be provided")

        self.model = model
        self.name = name
        self.output_dir = output_dir
        self.motif_save_path = os.path.join(output_dir, name)
        Path(self.motif_save_path).mkdir(parents=True, exist_ok=True)


    def prepare_data(self, sequences, labels, efficiencies=None):
        """
        Prepare DNA sequences and labels for motif analysis.

        Parameters:
        -----------
        sequences : list or numpy.ndarray
            DNA sequences as strings
        labels : list or numpy.ndarray
            Binary labels (1 for positive, 0 for negative)
        efficiencies : list or numpy.ndarray, optional
            Efficiency scores for the sequences

        Returns:
        --------
        X : torch.Tensor
            One-hot encoded DNA sequences
        y : torch.Tensor
            Binary labels as tensor
        q : pandas.Series or None
            Sorted efficiency scores (if provided)
        """
        X = representation(sequences, with_reverse=False)
        X = torch.tensor(X)
        y = torch.tensor(labels)

        # Sort by efficiency if provided
        q = None
        if efficiencies is not None:
            q = pd.Series(efficiencies)
            sort_indices = np.argsort(q)
            X = X[sort_indices]
            y = y[sort_indices]

        return X, y, q

    def analyze_from_dataframe(self, df, seq_col="sequence", label_col="label", eff_col=None):
        """
        Analyze motifs from a pandas DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame containing sequences and labels
        seq_col : str, default="sequence"
            Column name for DNA sequences
        label_col : str, default="label"
            Column name for binary labels (1 for positive, 0 for negative)
        eff_col : str, optional
            Column name for efficiency scores

        Returns:
        --------
        List of significant motifs and their statistics
        """
        sequences = df[seq_col].values
        labels = df[label_col].values
        efficiencies = df[eff_col].values if eff_col else None

        X, y, q = self.prepare_data(sequences, labels, efficiencies)
        return self.discover_motifs(X, y, q)
    def plot_pwm_logo(self, pwm, p_value, count):
        """
        Plot position weight matrix (PWM) as a sequence logo.

        Parameters:
        -----------
        pwm : numpy.ndarray
            Position weight matrix
        p_value : float
            Statistical significance (p-value)
        cluster_idx : int
            Cluster index for the motif
        """
        plt.figure(figsize=(12, 6))
        nucleotides = ["A", "C", "G", "T"]
        pwm_df = pd.DataFrame(pwm.T, columns=nucleotides)

        pwm_df += 1e-9
        entropy = -np.sum(pwm_df.apply(lambda x: x * np.log2(x)), axis=1)
        information_content = 2 - entropy
        scaled_pwm = pwm_df.mul(information_content, axis=0)
        logo = logomaker.Logo(scaled_pwm)
        plt.ylim([0, 2])
        plt.xlabel("Position")
        plt.ylabel("Information Content (bits)")
        plt.title(f"PWM Logo, p-value: {p_value:.2e}")
        plt.tight_layout()
        plt.savefig(
            f"{self.motif_save_path}/motif_No{count}_length{pwm.shape[1]}.png",
            dpi=200,
        )
        plt.close()

    def feature_attribution(self, X, y, q=None):
        """
        Perform feature attribution on sequences using DeepLift.

        Parameters:
        -----------
        X : torch.Tensor
            One-hot encoded DNA sequences
        y : torch.Tensor
            Binary labels
        q : pandas.Series, optional
            Efficiency scores

        Returns:
        --------
        tuple
            X, y, discovered PWMs, window sizes
        """
        seqs_attr = []
        dl = DeepLift(self.model)
        attributions = dl.attribute(X.float(), target=1)
        seqs_attr.append(attributions.detach().numpy())
        seqs_attr = np.vstack(seqs_attr)

        if q is not None:
            seqs_attr = seqs_attr[np.argsort(q.tolist())]
            y = y[np.argsort(q.tolist())]

        bot_seqs_attr = seqs_attr[np.where(y == 1)[0]]

        window_sizes = np.arange(4, 13)
        pwms_per_window_size = {}

        # Clustering on all window sizes
        for window_size_idx, window_size in enumerate(window_sizes):
            motifs_per_window_size = []
            for seq_idx in range(bot_seqs_attr.shape[0]):
                kmer_start, _ = find_most_significant_kmer_in_sequence(
                    bot_seqs_attr[seq_idx], window_size=window_size, stride=1
                )
                if kmer_start is not None:
                    kmer = bot_seqs_attr[
                           seq_idx, kmer_start: kmer_start + window_size, :
                           ]
                    alphabetic_kmer = one_hot_to_DNA((kmer != 0).astype(int))
                    if len(alphabetic_kmer) == window_size:
                        motifs_per_window_size.append(alphabetic_kmer)

            motifs_per_window_size = pd.Series(motifs_per_window_size)
            if len(motifs_per_window_size) == 0:
                continue

            unique_motifs = pd.Series(motifs_per_window_size.unique())
            distance_matrix = pd.DataFrame(
                pairwise_distance(unique_motifs),
                index=unique_motifs,
                columns=unique_motifs,
            )
            sample_weight = motifs_per_window_size.value_counts().loc[
                distance_matrix.index
            ]
            clusters, embeddings_2d = tsne_kmeans_search_silhouette(
                distance_matrix, sample_weight
            )
            embeddings_2d = pd.DataFrame(
                embeddings_2d, columns=["dim 1", "dim 2"], index=distance_matrix.index
            )
            embeddings_2d["occurrence"] = motifs_per_window_size.value_counts().loc[
                embeddings_2d.index
            ]
            embeddings_2d["cluster"] = clusters
            pwm = embeddings_2d[["cluster", "occurrence"]]
            pwm["sequence"] = pwm.index
            pwms = {}
            for cluster in pwm["cluster"].unique():
                cluster_df = pwm[pwm["cluster"] == cluster]
                pwms[cluster] = create_pwm_for_cluster(cluster_df)
            pwms_per_window_size[window_size] = pwms

        return X, y, pwms_per_window_size, window_sizes

    def discover_motifs(self, X, y, q=None, alpha=0.05):
        """
        Discover statistically significant motifs from sequences.

        Parameters:
        -----------
        X : torch.Tensor
            One-hot encoded DNA sequences
        y : torch.Tensor
            Binary labels
        q : pandas.Series, optional
            Efficiency scores
        alpha : float, default=0.05
            Significance threshold (will be Bonferroni-corrected)

        Returns:
        --------
        list
            Significant motifs and their statistics
        """
        X, y, pwms_per_window_size, window_sizes = self.feature_attribution(X, y, q)

        seqs_positive = X[torch.tensor(y) == 1].numpy()
        seqs_negative = X[torch.tensor(y) == 0].numpy()
        p_values_per_pwm = []

        for window_size_idx, window_size in enumerate(window_sizes):
            if window_size not in pwms_per_window_size:
                continue

            for cluster_idx, pwm in pwms_per_window_size[window_size].items():
                counts_positive = convolve_pwm_with_sequences(pwm, seqs_positive)
                counts_negative = convolve_pwm_with_sequences(pwm, seqs_negative)
                try:
                    chi2, p_value = perform_chi_squared_tests(
                        counts_positive, counts_negative
                    )
                    p_values_per_pwm.append(
                        [
                            pwm,
                            chi2,
                            p_value,
                            cluster_idx,
                            window_size_idx,
                            counts_positive,
                            counts_negative,
                        ]
                    )
                except ValueError:
                    pass

        # Apply Bonferroni correction
        if len(p_values_per_pwm) > 0:
            corrected_alpha = alpha / len(p_values_per_pwm)
            significant_motifs = [_ for _ in p_values_per_pwm if _[2] < corrected_alpha]

            # Save results
            with open(f"{self.motif_save_path}/significantly_enriched_motifs.pkl", "wb") as fp:
                pickle.dump(significant_motifs, fp)

            # Generate plots
            for count, (pwm, _, p_value, _, _, _, _) in enumerate(significant_motifs):
                self.plot_pwm_logo(pwm, p_value, count+1)

            return significant_motifs

        return []

    def visualize_stored_motifs(self):
        """
        Visualize previously discovered significant motifs.
        """
        motif_file = f"{self.motif_save_path}/significantly_enriched_motifs.pkl"
        if not os.path.exists(motif_file):
            print(f"No stored motifs found at {motif_file}")
            return

        with open(motif_file, "rb") as fp:
            p_values_per_pwm = pickle.load(fp)

        for count, (pwm, _, p_value, _, _, _, _) in enumerate(p_values_per_pwm):
            self.plot_pwm_logo(pwm, p_value, count+1)
    #
    def save_motifs_as_meme(self, output_file=None):
        """
        Save discovered motifs in MEME format for compatibility with other tools.

        Parameters:
        -----------
        output_file : str, optional
            Output file path (defaults to motif_save_path/motifs.meme)
        """
        if output_file is None:
            output_file = f"{self.motif_save_path}/motifs.meme"

        motif_file = f"{self.motif_save_path}/significantly_enriched_motifs.pkl"
        if not os.path.exists(motif_file):
            print(f"No stored motifs found at {motif_file}")
            return

        with open(motif_file, "rb") as fp:
            p_values_per_pwm = pickle.load(fp)

        # Generate MEME format file
        with open(output_file, 'w') as f:
            f.write("MEME version 4\n\n")
            f.write("ALPHABET= ACGT\n\n")
            f.write("strands: + -\n\n")
            f.write("Background letter frequencies\n")
            f.write("A 0.25 C 0.25 G 0.25 T 0.25\n\n")

            for idx, (pwm, _, p_value, cluster_idx, _, _, _) in enumerate(p_values_per_pwm):
                f.write(f"MOTIF motif_{idx + 1}\n")
                f.write(f"letter-probability matrix: alength= 4 w= {pwm.shape[1]} nsites= 20 E= {p_value:.2e}\n")

                for i in range(pwm.shape[1]):
                    f.write(f" {pwm[0, i]:.6f} {pwm[1, i]:.6f} {pwm[2, i]:.6f} {pwm[3, i]:.6f}\n")
                f.write("\n")

        print(f"Saved motifs in MEME format to {output_file}")