# valuevec/nn_model/train.py
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from .model import ValueVecModel

def train_model(df, vocab, embedding_dim=50, num_epochs=1000, learning_rate=0.01, label_col="label", plot=False):
    """
    Train the ValueVec neural model using cosine similarity loss.

    Args:
        df (DataFrame): Contains 'center_word', 'context_word', and label columns.
        vocab (list): List of all unique vocabulary words.
        embedding_dim (int): Dimensionality of embeddings.
        num_epochs (int): Number of epochs for training.
        learning_rate (float): Optimizer learning rate.
        label_col (str): Name of the column containing similarity scores in [0, 1].

    Returns:
        (Tensor, dict): Final learned embeddings and the word-to-index mapping.
    """
    # Create a word-to-index mapping for fast lookup
    word_to_index = {word: i for i, word in enumerate(vocab)}

    # Convert words to indices
    center_idx = torch.tensor([word_to_index[w] for w in df['center_word']], dtype=torch.long)
    context_idx = torch.tensor([word_to_index[w] for w in df['context_word']], dtype=torch.long)

    # Convert similarity scores from [0, 1] to [-1, 1] (cosine similarity range)
    labels = torch.tensor(df[label_col].values * 2 - 1, dtype=torch.float32)

    # Initialize the model
    model = ValueVecModel(len(vocab), embedding_dim)

    # Set up loss function (Mean Squared Error) and Adam optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Store loss per epoch for plotting
    losses = []

    for epoch in range(num_epochs):
        model.train()  # Set model to training mode

        # Forward pass: predict cosine similarity
        preds = model(center_idx, context_idx)

        # Compute loss between predicted similarities and target labels
        loss = criterion(preds, labels)

        # Backward pass and optimization
        optimizer.zero_grad()  # Clear gradients
        loss.backward()        # Compute gradients
        optimizer.step()       # Update weights

        # Log current loss
        losses.append(loss.item())

        # Print progress every 200 epochs
        if (epoch + 1) % 200 == 0:
            print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")

    # Plot and save the training loss curve
    if plot:
        plt.figure()
        plt.plot(losses)
        plt.title("Training Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.yscale("log")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("training_loss.png")
        print("Saved training_loss.png")

    # Return the learned embeddings and word-to-index map
    return model.embeddings.weight.detach(), word_to_index
