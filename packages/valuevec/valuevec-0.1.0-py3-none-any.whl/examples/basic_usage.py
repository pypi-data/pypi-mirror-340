# examples/basic_usage.py
"""
Basic usage example for ValueVec embeddings using the PyTorch NN model.
"""
import torch
import pandas as pd
from nn_model import  train_model, compute_similarity, get_most_similar
from training_data import create_color_spectrum_dataset

def main():
    # Create a simple dataset
    print("Creating color spectrum dataset...")
    color_df, vocab = create_color_spectrum_dataset(n_colors=15)
    
    # Create training pairs
    print("Creating training pairs...")
    from training_data import create_training_pairs
    
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
    
    # Train the model
    print("\nTraining the model...")
    embeddings, word_to_index = train_model(
        df=pairs_df,
        vocab=vocab,
        embedding_dim=10,
        num_epochs=500,
        learning_rate=0.05,
        plot=True
    )
    
    # Use the model for similarity calculations
    print("\nComputing similarities between colors:")
    pairs = [
        ("blue", "cyan"),
        ("red", "orange"),
        ("violet", "red")
    ]
    
    for word1, word2 in pairs:
        sim = compute_similarity(word1, word2, embeddings, word_to_index)
        print(f"Similarity between {word1} and {word2}: {sim:.4f}")
    
    # Find most similar colors
    print("\nMost similar colors:")
    for word in ["blue", "red", "green"]:
        similar = get_most_similar(word, embeddings, word_to_index, top_k=3)
        print(f"Colors most similar to {word}:")
        for similar_word, sim in similar:
            print(f"  - {similar_word}: {sim:.4f}")

if __name__ == "__main__":
    main()