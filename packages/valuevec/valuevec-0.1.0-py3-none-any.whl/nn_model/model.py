# valuevec/nn_model/model.py
import torch
import torch.nn as nn

class ValueVecModel(nn.Module):
    """
    Neural network model for learning value-based word embeddings using cosine similarity.
    This class defines an embedding layer and computes cosine similarity between word pairs.
    """
    def __init__(self, vocab_size: int, embedding_dim: int):
        """
        Initialize the ValueVecModel.

        Args:
            vocab_size (int): Total number of unique words in the vocabulary.
            embedding_dim (int): Dimensionality of the embedding space.
        """
        super(ValueVecModel, self).__init__()  # Call the parent constructor

        # Define an embedding layer to learn embeddings for each word
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)

        # Initialize embedding weights uniformly in the range [-0.1, 0.1]
        self.embeddings.weight.data.uniform_(-0.1, 0.1)

    def forward(self, center_idx, context_idx):
        """
        Compute cosine similarity between center and context word embeddings.

        Args:
            center_idx (Tensor): Tensor of indices for center words (shape: [batch_size])
            context_idx (Tensor): Tensor of indices for context words (shape: [batch_size])

        Returns:
            Tensor: Cosine similarity values for each word pair (shape: [batch_size])
        """
        # Look up embeddings for center and context word indices
        center_embed = self.embeddings(center_idx)   # shape: [batch_size, embedding_dim]
        context_embed = self.embeddings(context_idx) # shape: [batch_size, embedding_dim]

        # Compute dot product for each pair of vectors
        dot_product = torch.sum(center_embed * context_embed, dim=1)  # shape: [batch_size]

        # Compute L2 norm (magnitude) for each embedding
        center_norm = torch.norm(center_embed, dim=1)   # shape: [batch_size]
        context_norm = torch.norm(context_embed, dim=1) # shape: [batch_size]

        # Add epsilon to denominator to avoid division by zero
        epsilon = 1e-8
        cosine_similarity = dot_product / (center_norm * context_norm + epsilon)

        return cosine_similarity
