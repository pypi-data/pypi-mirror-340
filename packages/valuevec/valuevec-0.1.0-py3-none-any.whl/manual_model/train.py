"""
Functions for training ValueVec embeddings.
"""
import torch
import torch.nn.functional as F
from .embeddings import initialize_embeddings

def update_embeddings(df, main_embeddings, context_embeddings, word_to_index, learning_rate):
    """
    Update embeddings based on training data.
    
    Args:
        df (pandas.DataFrame): Training data with columns 'center_word', 'context_word', and 'label'
        main_embeddings (torch.Tensor): Main word embeddings
        context_embeddings (torch.Tensor): Context word embeddings
        word_to_index (dict): Mapping from words to indices
        learning_rate (float): Learning rate for updates
        
    Returns:
        tuple: Updated (main_embeddings, context_embeddings)
    """
    # Create copies to accumulate updates
    main_updates = torch.zeros_like(main_embeddings)
    context_updates = torch.zeros_like(context_embeddings)
    
    update_counts_main = torch.zeros(len(main_embeddings), dtype=torch.float)
    update_counts_context = torch.zeros(len(context_embeddings), dtype=torch.float)
    
    for i, row in df.iterrows():
        center_word = row['center_word']
        context_word = row['context_word']
        target_similarity = row['label']  # This is our target in range [0,1]
        
        center_idx = word_to_index[center_word]
        context_idx = word_to_index[context_word]
        
        # Retrieve current normalized embeddings
        u = F.normalize(main_embeddings[center_idx].unsqueeze(0), p=2, dim=1).squeeze()
        v = F.normalize(context_embeddings[context_idx].unsqueeze(0), p=2, dim=1).squeeze()
        
        # Current cosine similarity (dot product of normalized vectors)
        current_similarity = torch.dot(u, v)
        
        # Transform cosine similarity to [0,1] range using linear mapping
        current_mapped = (current_similarity + 1) / 2
        
        # Error: difference between current and target similarity
        error = current_mapped - target_similarity
        
        # Adjust gradient by chain rule for the mapping
        mapping_derivative = 0.5  # derivative of (x+1)/2 is 0.5
        error_adjusted = error * mapping_derivative
        
        # Calculate gradients for cosine similarity
        grad_u = v - current_similarity * u
        grad_v = u - current_similarity * v
        
        # Apply updates with error scaling
        main_updates[center_idx] -= learning_rate * error_adjusted * grad_u
        context_updates[context_idx] -= learning_rate * error_adjusted * grad_v
        
        update_counts_main[center_idx] += 1
        update_counts_context[context_idx] += 1
    
    # Average the updates
    for i in range(len(main_embeddings)):
        if update_counts_main[i] > 0:
            main_embeddings[i] += main_updates[i] / update_counts_main[i]
    
    for i in range(len(context_embeddings)):
        if update_counts_context[i] > 0:
            context_embeddings[i] += context_updates[i] / update_counts_context[i]
    
    # Normalize after applying updates
    main_embeddings = F.normalize(main_embeddings, p=2, dim=1)
    context_embeddings = F.normalize(context_embeddings, p=2, dim=1)
    
    return main_embeddings, context_embeddings

def train_model(df, vocab, embedding_dim=10, num_epochs=10000, learning_rate=0.01):
    """
    Train the embedding model using the training pairs.
    
    Args:
        df (pandas.DataFrame): Training data with columns 'center_word', 'context_word', and 'label'
        vocab (list): List of vocabulary words
        embedding_dim (int): Dimension of the embedding vectors
        num_epochs (int): Number of training epochs
        learning_rate (float): Learning rate for updates
        
    Returns:
        tuple: (final_embeddings, word_to_index)
            - final_embeddings: Trained word embeddings
            - word_to_index: Mapping from words to indices
    """
    # Initialize embeddings
    main_embeddings, context_embeddings, word_to_index = initialize_embeddings(
        vocab, embedding_dim
    )
    
    # Training loop with adaptive learning rate
    best_avg_error = float('inf')
    patience = 10
    patience_counter = 0
    
    for epoch in range(num_epochs):
        # Shuffle data
        df_shuffled = df.sample(frac=1).reset_index(drop=True)
        
        # Update embeddings
        main_embeddings, context_embeddings = update_embeddings(
            df_shuffled, main_embeddings, context_embeddings, word_to_index, learning_rate
        )
        
        # Calculate average error for monitoring
        if (epoch + 1) % 10 == 0:
            total_error = 0.0
            for i, row in df.iterrows():
                center_idx = word_to_index[row['center_word']]
                context_idx = word_to_index[row['context_word']]
                
                u = F.normalize(main_embeddings[center_idx].unsqueeze(0), p=2, dim=1).squeeze()
                v = F.normalize(context_embeddings[context_idx].unsqueeze(0), p=2, dim=1).squeeze()
                
                sim = torch.dot(u, v).item()
                mapped_sim = (sim + 1) / 2  # Map from [-1,1] to [0,1]
                target = row['label']
                
                total_error += abs(mapped_sim - target)
            
            avg_error = total_error / len(df)
            print(f"Epoch {epoch + 1}/{num_epochs}, Avg Error: {avg_error:.4f}")
            
            # Early stopping logic
            if avg_error < best_avg_error:
                best_avg_error = avg_error
                patience_counter = 0
            else:
                patience_counter += 1
                
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch + 1}")
                break
    
    # Average the two embedding spaces for final representation
    final_embeddings = (main_embeddings + context_embeddings) / 2
    final_embeddings = F.normalize(final_embeddings, p=2, dim=1)
    
    return final_embeddings, word_to_index
