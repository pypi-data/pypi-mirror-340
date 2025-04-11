# valuevec/nn_model/visualization.py
"""
Visualization utilities for ValueVec embeddings.
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def plot_embeddings(embeddings, word_to_index, title="Word Embeddings Visualization", 
                   method="pca", n_components=2, words_to_show=None, figsize=(12, 8),
                   annotate=True, save_path=None):
    """
    Visualize word embeddings in 2D space using dimensionality reduction.
    
    Args:
        embeddings (torch.Tensor): The embedding matrix
        word_to_index (dict): Mapping from words to indices
        title (str): Plot title
        method (str): Dimensionality reduction method ('pca' or 'tsne')
        n_components (int): Number of components for dimensionality reduction
        words_to_show (list): List of specific words to visualize (if None, show all)
        figsize (tuple): Figure size for the plot
        annotate (bool): Whether to add word labels
        save_path (str): Path to save the plot (if None, display instead)
        
    Returns:
        pyplot.Figure: The figure object
    """
    # Convert embeddings to numpy for sklearn compatibility
    embeddings_np = embeddings.detach().numpy() if hasattr(embeddings, 'detach') else np.array(embeddings)
    
    # Create reverse mapping (index to word)
    index_to_word = {idx: word for word, idx in word_to_index.items()}
    
    # Filter words if specified
    if words_to_show is not None:
        indices = [word_to_index[word] for word in words_to_show if word in word_to_index]
        embeddings_to_plot = embeddings_np[indices]
        words_to_plot = [index_to_word[idx] for idx in indices]
    else:
        embeddings_to_plot = embeddings_np
        words_to_plot = [index_to_word[i] for i in range(len(embeddings_np))]
    
    # Apply dimensionality reduction
    if method.lower() == 'tsne':
        model = TSNE(n_components=n_components, random_state=42, perplexity=min(30, len(embeddings_to_plot)-1))
    else:  # default to PCA
        model = PCA(n_components=n_components)
    
    # Reduce dimensions
    reduced = model.fit_transform(embeddings_to_plot)
    
    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot points
    ax.scatter(reduced[:, 0], reduced[:, 1], s=100, alpha=0.6)
    
    # Add labels
    if annotate:
        for i, word in enumerate(words_to_plot):
            ax.annotate(word, (reduced[i, 0], reduced[i, 1]), 
                       fontsize=11, alpha=0.7)
    
    # Set title and labels
    ax.set_title(title)
    ax.set_xlabel(f"Component 1")
    ax.set_ylabel(f"Component 2")
    ax.grid(alpha=0.3)
    
    # Add method info
    plt.figtext(0.99, 0.01, f"Method: {method.upper()}", 
                horizontalalignment='right', fontsize=8)
    
    plt.tight_layout()
    
    # Save or display
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    
    return fig