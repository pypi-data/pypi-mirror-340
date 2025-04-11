"""
Data generation utilities for ValueVec.
"""
import pandas as pd
import random
import numpy as np
from .training_pairs import create_training_pairs


def create_color_spectrum_dataset(n_colors=20, random_seed=42):
    """
    Create a simple dataset of colors positioned along the visible light spectrum.
    
    Args:
        n_colors: Number of colors to generate
        random_seed: Random seed for reproducibility
    
    Returns:
        DataFrame with color names and their position values (wavelength)
        vocabulary: List of all unique color names
    """
    # Set random seed for reproducibility
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    # Base colors in spectrum order (roughly corresponding to wavelength)
    base_colors = [
        "violet", "indigo", "blue", "cyan", "teal", "green", 
        "chartreuse", "yellow", "gold", "orange", "red", "crimson"
    ]
    
    # Generate derived color names by adding modifiers
    modifiers = ["light", "dark", "vivid", "pale", "deep", "bright"]
    
    colors = base_colors.copy()
    while len(colors) < n_colors:
        base = random.choice(base_colors)
        modifier = random.choice(modifiers)
        new_color = f"{modifier}-{base}"
        if new_color not in colors:
            colors.append(new_color)
    
    # Trim to exact number requested
    colors = colors[:n_colors]
    
    # Assign positions along the spectrum (wavelength in nm, approximately)
    # Violet ~380nm to Red ~750nm
    base_positions = {
        "violet": 380,
        "indigo": 420,
        "blue": 460,
        "cyan": 490,
        "teal": 510,
        "green": 530,
        "chartreuse": 560,
        "yellow": 580,
        "gold": 600,
        "orange": 620,
        "red": 680,
        "crimson": 730
    }
    
    # Function to get position, adding small noise for modifiers
    def get_position(color):
        if color in base_positions:
            return base_positions[color]
        else:
            # For derived colors, extract the base
            parts = color.split('-')
            modifier = parts[0]
            base = parts[1]
            
            base_pos = base_positions[base]
            
            # Modifiers shift the position slightly
            modifier_shifts = {
                "light": -10,
                "dark": +10,
                "vivid": -5,
                "pale": -15,
                "deep": +15,
                "bright": -8
            }
            
            shift = modifier_shifts.get(modifier, 0)
            # Add a small random noise
            noise = np.random.normal(0, 3)
            
            return base_pos + shift + noise
    
    # Create the dataset
    df = pd.DataFrame({
        "keyword": colors,
        "estimated_value": [get_position(color) for color in colors]
    })
    
    # Sort by wavelength to see the spectrum order
    df = df.sort_values("estimated_value").reset_index(drop=True)
    
    # Create vocabulary list
    vocabulary = df["keyword"].tolist()
    
    print(f"Created dataset with {len(df)} colors along the visible spectrum")
    print(df.head())
    
    return df, vocabulary


def create_color_training_pairs(color_df, random_seed=42, label_col="label"):
    """
    Create training pairs for colors with similarity based on their position in the spectrum.
    
    Args:
        color_df: DataFrame with colors and their estimated_value (wavelength)
        random_seed: Random seed for reproducibility
        label_col: Name of the column for similarity scores
        
    Returns:
        DataFrame with center_word, context_word and similarity label columns
    """
    # Make a copy to avoid modifying the original
    df_norm = color_df.copy()
    
    # Calculate normalized wavelength values (0-1 range)
    min_val = df_norm['estimated_value'].min()
    max_val = df_norm['estimated_value'].max()
    df_norm['normalized_value'] = (df_norm['estimated_value'] - min_val) / (max_val - min_val)
    
    # Ensure the data is properly sorted by wavelength
    df_norm = df_norm.sort_values('estimated_value').reset_index(drop=True)
    
    # Use the enhanced create_training_pairs function with focus_attribute
    return create_training_pairs(
        data=df_norm,
        item_col='keyword',
        focus_attribute='normalized_value',  # Focus on normalized wavelength
        include_attribute_values=True,       # Include the normalized values
        value_col='normalized_value',        # Specifically use normalized_value
        sort_by='estimated_value',           # Sort by original wavelength
        sort_ascending=True,                 # Low to high wavelength
        context_window_size=2,               # Consider 2 colors before/after
        num_negatives=3,                     # Add 3 negative examples per color
        negative_sample_strategy="extreme",  # Use colors from opposite ends
        label_col=label_col,                 # Use specified label column name
        random_seed=random_seed              # For reproducibility
    )

def create_animal_dataset(n_animals=30, random_seed=42):
    """
    Create a dataset of animals with various attributes.
    
    Args:
        n_animals: Number of animals to include
        random_seed: Random seed for reproducibility
    
    Returns:
        DataFrame with animal names and their attribute values
        vocabulary: List of all unique animal names
    """
    # Set random seed for reproducibility
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    # Base animals
    animals = [
        "cat", "dog", "horse", "elephant", "mouse", "lion", "tiger", "bear", 
        "wolf", "fox", "rabbit", "deer", "giraffe", "zebra", "hippo", 
        "monkey", "gorilla", "eagle", "hawk", "penguin", "fish", "shark",
        "dolphin", "whale", "snake", "lizard", "turtle", "frog", "ant", "bee"
    ]
    
    # Trim to exact number requested
    animals = animals[:n_animals]
    
    # Create attributes (size in kg, speed in km/h, lifespan in years)
    attributes = {
        "cat": {"size": 5, "speed": 48, "lifespan": 15},
        "dog": {"size": 30, "speed": 45, "lifespan": 13},
        "horse": {"size": 700, "speed": 88, "lifespan": 25},
        "elephant": {"size": 5000, "speed": 40, "lifespan": 70},
        "mouse": {"size": 0.02, "speed": 13, "lifespan": 2},
        "lion": {"size": 190, "speed": 80, "lifespan": 15},
        "tiger": {"size": 220, "speed": 65, "lifespan": 16},
        "bear": {"size": 600, "speed": 56, "lifespan": 25},
        "wolf": {"size": 80, "speed": 60, "lifespan": 13},
        "fox": {"size": 14, "speed": 50, "lifespan": 12},
        "rabbit": {"size": 2, "speed": 56, "lifespan": 9},
        "deer": {"size": 90, "speed": 80, "lifespan": 10},
        "giraffe": {"size": 1200, "speed": 60, "lifespan": 25},
        "zebra": {"size": 350, "speed": 64, "lifespan": 25},
        "hippo": {"size": 1500, "speed": 30, "lifespan": 45},
        "monkey": {"size": 15, "speed": 35, "lifespan": 20},
        "gorilla": {"size": 180, "speed": 40, "lifespan": 40},
        "eagle": {"size": 6, "speed": 160, "lifespan": 20},
        "hawk": {"size": 1.5, "speed": 190, "lifespan": 20},
        "penguin": {"size": 30, "speed": 9, "lifespan": 20},
        "fish": {"size": 1, "speed": 12, "lifespan": 5},
        "shark": {"size": 900, "speed": 56, "lifespan": 30},
        "dolphin": {"size": 150, "speed": 37, "lifespan": 25},
        "whale": {"size": 40000, "speed": 47, "lifespan": 90},
        "snake": {"size": 10, "speed": 32, "lifespan": 15},
        "lizard": {"size": 0.5, "speed": 29, "lifespan": 10},
        "turtle": {"size": 200, "speed": 10, "lifespan": 100},
        "frog": {"size": 0.05, "speed": 5, "lifespan": 8},
        "ant": {"size": 0.001, "speed": 2, "lifespan": 1},
        "bee": {"size": 0.0001, "speed": 24, "lifespan": 1}
    }
    
    # Create the dataset
    df = pd.DataFrame({
        "animal": animals,
        "size": [attributes[animal]["size"] for animal in animals],
        "speed": [attributes[animal]["speed"] for animal in animals],
        "lifespan": [attributes[animal]["lifespan"] for animal in animals]
    })
    
    # Add a small random noise to make it more realistic
    df["size"] *= np.random.normal(1, 0.05, len(df))
    df["speed"] *= np.random.normal(1, 0.05, len(df))
    df["lifespan"] *= np.random.normal(1, 0.05, len(df))
    
    # Create vocabulary list
    vocabulary = df["animal"].tolist()
    
    print(f"Created dataset with {len(df)} animals")
    print(df.head())
    
    return df, vocabulary

def create_animal_training_pairs(animal_df, primary_attribute=None, attribute_weights=None, 
                         random_seed=42, label_col="label"):
    """
    Create training pairs of animals with similarity labels based on their attributes.
    
    Args:
        animal_df: DataFrame with animals and their attributes
        primary_attribute: Primary attribute to focus on for similarity (e.g., 'speed')
                          If specified, this attribute will have higher weight
        attribute_weights: Optional dict mapping attributes to weights
                          If not provided, weights will be generated based on primary_attribute
        random_seed: Random seed for reproducibility
        label_col: Name of the column for similarity scores in the output
    
    Returns:
        DataFrame with center_word, context_word and similarity label pairs
    """
    # Normalize attributes for similarity calculation
    df_norm = animal_df.copy()
    attributes = ['size', 'speed', 'lifespan']
    
    for col in attributes:
        # Log-transform size due to large range
        if col == 'size':
            df_norm[col] = np.log(df_norm[col])
        
        # Min-max normalization
        min_val = df_norm[col].min()
        max_val = df_norm[col].max()
        df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
    
    # Set up attribute weights
    if attribute_weights is None:
        if primary_attribute is not None and primary_attribute in attributes:
            # Give higher weight to primary attribute
            attribute_weights = {attr: 0.15 for attr in attributes}  # Base weight
            attribute_weights[primary_attribute] = 0.7  # Primary attribute gets 70% weight
        else:
            # Default weights if no primary attribute specified
            attribute_weights = {'size': 0.4, 'speed': 0.3, 'lifespan': 0.3}
    
    # Normalize weights to sum to 1
    total_weight = sum(attribute_weights.values())
    attribute_weights = {k: v / total_weight for k, v in attribute_weights.items()}
    
    print(f"Using attribute weights: {attribute_weights}")
    
    # Define similarity function for animals
    def animal_similarity(animal1, animal2):
        # Calculate similarity based on weighted attributes
        similarity = 0.0
        for attr, weight in attribute_weights.items():
            # Calculate similarity for this attribute (1 - normalized difference)
            attr_sim = 1.0 - abs(animal1[attr] - animal2[attr])
            # Add weighted contribution to overall similarity
            similarity += weight * attr_sim
        return similarity
    
    # Sort by primary attribute if specified
    sort_by = primary_attribute if primary_attribute in attributes else None
    
    # Use the generic create_training_pairs function
    return create_training_pairs(
        data=df_norm,
        item_col='animal',
        similarity_fn=animal_similarity,
        attributes=attributes,
        num_negatives=1,
        context_window_size=1,
        random_seed=random_seed,
        label_col=label_col,
        sort_by=sort_by,
        include_attribute_values=True,
        value_col=primary_attribute if primary_attribute else None
    )





