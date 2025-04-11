# examples/manual_vs_nn_compare.py
"""
Comparison between manual and neural network implementations of ValueVec.
"""
import time
import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Import both implementations - fix import paths
from manual_model.train import train_model as train_manual
from manual_model.embeddings import compute_similarity as compute_sim_manual
from nn_model.train import train_model as train_nn
from nn_model.utils import compute_similarity as compute_sim_nn
from training_data.data import create_color_spectrum_dataset
from training_data.training_pairs import create_training_pairs

def run_benchmark():
    # Create dataset
    color_df, vocab = create_color_spectrum_dataset(n_colors=20)
    
    # Normalize the values
    color_df['normalized'] = (color_df['estimated_value'] - color_df['estimated_value'].min()) / \
                            (color_df['estimated_value'].max() - color_df['estimated_value'].min())
    
    pairs_df = create_training_pairs(
        data=color_df,
        item_col='keyword',
        focus_attribute='normalized',
        context_window_size=2,
        num_negatives=2
    )
    
    # Configuration for comparison
    embedding_dims = [5, 10, 20]
    
    # Results storage
    training_times = {'manual': [], 'nn': []}
    similarity_results = {'manual': {}, 'nn': {}}
    
    # Define some pairs to test
    test_pairs = [
        ("blue", "cyan"),      # Close in spectrum
        ("violet", "yellow"),  # Further apart
        ("red", "green")       # Far apart
    ]
    
    # Run both implementations at different embedding sizes
    for dim in embedding_dims:
        print(f"\nTesting with embedding dimension = {dim}")
        
        # Manual implementation
        print("Training manual model...")
        start_time = time.time()
        manual_embeddings, manual_word_to_idx = train_manual(
            df=pairs_df,
            vocab=vocab,
            embedding_dim=dim,
            num_epochs=300,
            learning_rate=0.05
        )
        manual_time = time.time() - start_time
        training_times['manual'].append(manual_time)
        print(f"Manual training completed in {manual_time:.2f} seconds")
        
        # Neural network implementation
        print("Training neural network model...")
        start_time = time.time()
        nn_embeddings, nn_word_to_idx = train_nn(
            df=pairs_df,
            vocab=vocab,
            embedding_dim=dim,
            num_epochs=300,
            learning_rate=0.05
        )
        nn_time = time.time() - start_time
        training_times['nn'].append(nn_time)
        print(f"NN training completed in {nn_time:.2f} seconds")
        
        # Compare similarity results
        similarity_results['manual'][dim] = []
        similarity_results['nn'][dim] = []
        
        print(f"\nSimilarity comparisons (dim={dim}):")
        for word1, word2 in test_pairs:
            manual_sim = compute_sim_manual(word1, word2, manual_embeddings, manual_word_to_idx)
            nn_sim = compute_sim_nn(word1, word2, nn_embeddings, nn_word_to_idx)
            
            similarity_results['manual'][dim].append(manual_sim)
            similarity_results['nn'][dim].append(nn_sim)
            
            print(f"{word1} - {word2}: Manual={manual_sim:.4f}, NN={nn_sim:.4f}, Diff={abs(manual_sim-nn_sim):.4f}")
    
    # Plot results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Training time comparison
    ax1.plot(embedding_dims, training_times['manual'], 'o-', label='Manual')
    ax1.plot(embedding_dims, training_times['nn'], 's-', label='Neural Network')
    ax1.set_xlabel('Embedding Dimensions')
    ax1.set_ylabel('Training Time (seconds)')
    ax1.set_title('Training Time Comparison')
    ax1.legend()
    ax1.grid(True)
    
    # Similarity comparison
    width = 0.35
    x = np.arange(len(test_pairs))
    
    # Use the middle embedding dimension for the comparison
    mid_dim = embedding_dims[len(embedding_dims)//2]
    
    ax2.bar(x - width/2, similarity_results['manual'][mid_dim], width, label='Manual')
    ax2.bar(x + width/2, similarity_results['nn'][mid_dim], width, label='Neural Network')
    
    ax2.set_xlabel('Word Pairs')
    ax2.set_ylabel('Cosine Similarity')
    ax2.set_title(f'Similarity Comparison (dim={mid_dim})')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"{p[0]}-{p[1]}" for p in test_pairs])
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('model_comparison.png')
    print("\nSaved comparison results to model_comparison.png")

if __name__ == "__main__":
    run_benchmark()