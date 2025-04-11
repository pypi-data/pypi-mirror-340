# valuevec/nn_model/utils.py
import torch

def compute_similarity(word1, word2, embeddings, word_to_index):
    """
    Compute cosine similarity between two words using their embeddings.

    Args:
        word1 (str): The first word.
        word2 (str): The second word.
        embeddings (Tensor): The learned word embeddings.
        word_to_index (dict): Mapping from word to index in embedding matrix.

    Returns:
        float: Cosine similarity between the two word vectors.
    """
    if word1 not in word_to_index or word2 not in word_to_index:
        return 0.0  # Return 0 if either word is not in the vocabulary

    # Get index of each word
    idx1 = word_to_index[word1]
    idx2 = word_to_index[word2]

    # Retrieve corresponding embeddings
    vec1 = embeddings[idx1]
    vec2 = embeddings[idx2]

    # Compute cosine similarity = dot(a, b) / (||a|| * ||b||)
    dot = torch.dot(vec1, vec2).item()
    norm = torch.norm(vec1).item() * torch.norm(vec2).item()

    return dot / (norm + 1e-8)  # Add epsilon to avoid division by zero

def get_most_similar(word, embeddings, word_to_index, top_k=5):
    """
    Retrieve the top_k most similar words to the input word based on cosine similarity.

    Args:
        word (str): Target word to find similarities for.
        embeddings (Tensor): The embedding matrix.
        word_to_index (dict): Mapping from word to index.
        top_k (int): Number of top similar words to return.

    Returns:
        list: List of (word, similarity) tuples sorted by similarity (descending).
    """
    if word not in word_to_index:
        return []  # Return empty if the word is not in the vocabulary

    # Retrieve the target word's embedding
    idx = word_to_index[word]
    query_vec = embeddings[idx]

    # Normalize the query vector
    query_vec = query_vec / (torch.norm(query_vec) + 1e-8)

    # Compute cosine similarity between query vector and all other embeddings
    sims = torch.matmul(embeddings, query_vec)  # shape: [vocab_size]

    # Exclude the word itself by setting similarity to -inf
    sims[idx] = -float("inf")

    # Get indices of top_k most similar words
    top_indices = torch.topk(sims, top_k).indices.tolist()

    # Reverse mapping from index to word
    index_to_word = {i: w for w, i in word_to_index.items()}

    # Return list of (word, similarity) pairs
    return [(index_to_word[i], sims[i].item()) for i in top_indices]