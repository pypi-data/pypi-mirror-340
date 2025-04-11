"""
Core functionality for handling ValueVec embeddings.
"""
import torch
import torch.nn.functional as F

def initialize_embeddings(vocab, embedding_dim=5):
    """
    Initialize embeddings for the main and context words.
    
    Args:
        vocab (list): List of vocabulary words
        embedding_dim (int): Dimension of the embedding vectors
        
    Returns:
        tuple: (main_embeddings, context_embeddings, word_to_index)
            - main_embeddings: Tensor of shape (vocab_size, embedding_dim)
            - context_embeddings: Tensor of shape (vocab_size, embedding_dim)
            - word_to_index: Dictionary mapping words to their indices
    """
    vocab_size = len(vocab)
    
    # Create word-to-index mapping
    word_to_index = {word: idx for idx, word in enumerate(vocab)}
    
    # Initialize embeddings randomly
    main_embeddings = torch.randn(vocab_size, embedding_dim) * 0.1
    context_embeddings = torch.randn(vocab_size, embedding_dim) * 0.1
    
    # Normalize embeddings
    main_embeddings = F.normalize(main_embeddings, p=2, dim=1)
    context_embeddings = F.normalize(context_embeddings, p=2, dim=1)
    
    return main_embeddings, context_embeddings, word_to_index

def compute_similarity(word1, word2, embeddings, word_to_index):
    """
    Compute cosine similarity between two words using their embeddings.
    
    Args:
        word1 (str): First word
        word2 (str): Second word
        embeddings (torch.Tensor): The embedding matrix
        word_to_index (dict): Mapping from words to indices
        
    Returns:
        float: Cosine similarity between the two word embeddings
    """
    # Get word indices
    idx1 = word_to_index.get(word1)
    idx2 = word_to_index.get(word2)
    
    if idx1 is None or idx2 is None:
        raise ValueError(f"Word not in vocabulary: {word1 if idx1 is None else word2}")
    
    # Get embeddings
    emb1 = embeddings[idx1]
    emb2 = embeddings[idx2]
    
    # Normalize (in case embeddings aren't already normalized)
    emb1 = F.normalize(emb1.unsqueeze(0), p=2, dim=1).squeeze()
    emb2 = F.normalize(emb2.unsqueeze(0), p=2, dim=1).squeeze()
    
    # Compute cosine similarity
    similarity = torch.dot(emb1, emb2).item()
    
    return similarity

def get_most_similar(word, embeddings, word_to_index, top_k=5):
    """
    Find the top_k most similar words to the given word.

    Args:
        word (str): The query word
        embeddings (torch.Tensor): The embedding matrix
        word_to_index (dict): Mapping from words to indices
        top_k (int): Number of similar words to return

    Returns:
        list: List of (word, similarity) tuples for the most similar words
    """
    if word not in word_to_index:
        raise ValueError(f"Word not in vocabulary: {word}")

    idx = word_to_index[word]
    query_embedding = embeddings[idx]

    # Normalize query embedding
    query_embedding = F.normalize(query_embedding.unsqueeze(0), p=2, dim=1).squeeze()

    # Compute cosine similarity to all other words
    similarities = torch.matmul(embeddings, query_embedding)

    # Mask out the query word by setting its similarity to -inf
    similarities[idx] = -float('inf')

    # Get top k similar word indices
    top_indices = torch.topk(similarities, top_k).indices.tolist()

    # Create reverse mapping
    index_to_word = {i: w for w, i in word_to_index.items()}

    # Return results as (word, similarity) tuples
    results = [(index_to_word[i], similarities[i].item()) for i in top_indices]

    return results

