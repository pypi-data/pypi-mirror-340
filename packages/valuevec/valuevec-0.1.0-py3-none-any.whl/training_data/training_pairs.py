"""
Training pair generation utilities for ValueVec.

This module provides a generic function to generate training pairs from any dataset
for use in training embedding models, with advanced functionality for controlling
the distribution and quality of positive and negative training examples.
"""
import pandas as pd
import numpy as np
import random
from typing import List, Dict, Tuple, Union, Optional, Callable, Any


def create_training_pairs(
    data: pd.DataFrame,
    item_col: str,
    similarity_fn: Callable[[pd.Series, pd.Series], float] = None,
    focus_attribute: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    attribute_weights: Optional[Dict[str, float]] = None,
    noise_level: float = 0.05,
    random_seed: int = 42,
    min_similarity: float = 0.1,
    max_similarity: float = 0.9,
    context_window_size: int = 2,
    num_negatives: int = 3,
    sort_by: Optional[str] = None,
    sort_ascending: bool = True,
    negative_sample_strategy: str = "random",
    min_distance_pct: float = 0.25,
    include_pair_type: bool = True,
    include_attribute_values: bool = False,
    value_col: Optional[str] = None,
    label_col: str = "label",
    report_stats: bool = True,
) -> pd.DataFrame:
    """
    Generic function to create training pairs with similarity labels based on item attributes.
    
    Args:
        data: DataFrame containing items and their attributes
        item_col: Column name that contains the item identifiers (e.g., 'animal', 'fruit')
        similarity_fn: Function that calculates similarity between two items
        attributes: List of attribute columns to use for similarity calculation
                   (Not needed if similarity_fn doesn't use attributes)
        noise_level: Amount of random noise to add to similarity values
        random_seed: Random seed for reproducibility
        min_similarity: Minimum similarity value after adding noise
        max_similarity: Maximum similarity value after adding noise
        context_window_size: If using ordered data, number of items before/after to use as positive pairs
        num_negatives: Number of negative samples per center item
        sort_by: Column to sort the data by before creating pairs (if None, uses existing order)
        sort_ascending: Whether to sort in ascending order
        negative_sample_strategy: Strategy for sampling negative examples:
                                 "random" - completely random sampling
                                 "distance" - sample items further away in the sorted order
                                 "extreme" - prioritize items at the extreme ends
        min_distance_pct: Minimum distance (as percentage of dataset size) for negative sampling
        include_pair_type: Whether to include a "pair_type" column in the output
        include_attribute_values: Whether to include the attribute values in the output
        value_col: If include_attribute_values is True, which column to include as the value
                  (if None and sort_by is specified, uses sort_by)
        report_stats: Whether to print statistics about the generated pairs
    
    Returns:
        DataFrame with center_word, context_word and similarity label pairs
    """
    np.random.seed(random_seed)
    random.seed(random_seed)
    
    # Copy the data to avoid modifying the original
    df = data.copy()
    
    # If a focus attribute is provided but no similarity function,
    # create a default similarity function based on the focus attribute
    if focus_attribute is not None and similarity_fn is None:
        if focus_attribute in df.columns:
            # Set sort_by to focus_attribute if not specified
            if sort_by is None:
                sort_by = focus_attribute
                print(f"Sorting by focus attribute: {focus_attribute}")
            
            # Set value_col to focus_attribute if not specified and include_attribute_values
            if value_col is None and include_attribute_values:
                value_col = focus_attribute
            
            # Create a default similarity function based on the focus attribute
            def default_similarity_fn(item1, item2):
                # Normalize difference to [0,1] range
                diff = abs(item1[focus_attribute] - item2[focus_attribute])
                # Quadratic similarity falloff (sharper difference penalty)
                similarity = max(0.1, 1.0 - (diff * 2.0)**2)
                return similarity
            
            similarity_fn = default_similarity_fn
            print(f"Using default similarity function based on {focus_attribute}")
        else:
            raise ValueError(f"Focus attribute '{focus_attribute}' not found in dataset columns")
    
    # If attribute_weights are provided but no similarity function, create a weighted similarity function
    elif attribute_weights is not None and similarity_fn is None and attributes is not None:
        # Verify all weighted attributes exist
        missing_attrs = [attr for attr in attribute_weights.keys() if attr not in df.columns]
        if missing_attrs:
            raise ValueError(f"Attributes {missing_attrs} not found in dataset columns")
        
        # Normalize weights to sum to 1
        total_weight = sum(attribute_weights.values())
        normalized_weights = {k: v / total_weight for k, v in attribute_weights.items()}
        
        print(f"Using weighted similarity with weights: {normalized_weights}")
        
        # Create a weighted similarity function
        def weighted_similarity_fn(item1, item2):
            similarity = 0.0
            for attr, weight in normalized_weights.items():
                # Calculate similarity for this attribute (1 - normalized difference)
                attr_diff = abs(item1[attr] - item2[attr])
                attr_sim = max(0.1, 1.0 - attr_diff**2)  # Quadratic falloff
                # Add weighted contribution to overall similarity
                similarity += weight * attr_sim
            return similarity
        
        similarity_fn = weighted_similarity_fn
    
    # If no similarity function is provided at all, raise an error
    if similarity_fn is None:
        raise ValueError("Either similarity_fn, focus_attribute, or attribute_weights must be provided")
    
    # Sort data if requested
    if sort_by:
        df = df.sort_values(by=sort_by, ascending=sort_ascending).reset_index(drop=True)
    
    # Determine value column for reporting
    if include_attribute_values:
        if value_col is None and sort_by:
            value_col = sort_by
        elif value_col is None and attributes and len(attributes) > 0:
            value_col = attributes[0]
    
    # Extract items
    items = df[item_col].tolist()
    n = len(items)
    
    # Calculate minimum distance for negative sampling
    min_distance = max(1, int(n * min_distance_pct))
    
    center_words = []
    context_words = []
    labels = []
    pair_types = []
    center_values = []
    context_values = []
    
    for i, center_item in enumerate(items):
        center_item_data = df.iloc[i]
        
        # --- POSITIVE PAIRS ---
        # If using context window approach
        if context_window_size > 0:
            for j in range(1, context_window_size + 1):
                # Items before the center item
                if i - j >= 0:
                    _add_pair(
                        i, i-j, center_item, items[i-j], center_item_data, df.iloc[i-j],
                        similarity_fn, noise_level, min_similarity, max_similarity,
                        center_words, context_words, labels, pair_types, 
                        center_values, context_values, value_col, "positive"
                    )
                
                # Items after the center item
                if i + j < n:
                    _add_pair(
                        i, i+j, center_item, items[i+j], center_item_data, df.iloc[i+j],
                        similarity_fn, noise_level, min_similarity, max_similarity,
                        center_words, context_words, labels, pair_types, 
                        center_values, context_values, value_col, "positive"
                    )
        else:
            # Use all other items and let similarity function determine positive/negative
            for j in range(n):
                if i != j:  # Don't pair an item with itself
                    _add_pair(
                        i, j, center_item, items[j], center_item_data, df.iloc[j],
                        similarity_fn, noise_level, min_similarity, max_similarity,
                        center_words, context_words, labels, pair_types, 
                        center_values, context_values, value_col, "all"
                    )
            
        # --- NEGATIVE PAIRS ---
        # Only add explicit negative pairs if using context window approach
        if context_window_size > 0:
            neg_indices = []
            
            if negative_sample_strategy == "extreme":
                # Add furthest item as guaranteed negative
                furthest_idx = 0 if i > n/2 else n-1
                neg_indices.append(furthest_idx)
                
                # Add more random distant items
                remaining_negatives = num_negatives - 1
                
                # Define distant indices (items at least min_distance away)
                distant_indices = list(range(0, max(0, i-min_distance))) + list(range(min(n-1, i+min_distance), n))
                
                if distant_indices and remaining_negatives > 0:
                    # Sample without replacement if possible
                    sample_size = min(remaining_negatives, len(distant_indices))
                    sampled_indices = random.sample(distant_indices, sample_size)
                    neg_indices.extend(sampled_indices)
                    
            elif negative_sample_strategy == "distance":
                # Define distant indices (items at least min_distance away)
                distant_indices = list(range(0, max(0, i-min_distance))) + list(range(min(n-1, i+min_distance), n))
                
                if distant_indices and num_negatives > 0:
                    # Sample without replacement if possible
                    sample_size = min(num_negatives, len(distant_indices))
                    neg_indices = random.sample(distant_indices, sample_size)
                    
            else:  # "random"
                # Sample any index except within context window
                valid_indices = [j for j in range(n) if abs(j - i) > context_window_size and j != i]
                
                if valid_indices and num_negatives > 0:
                    # Sample without replacement if possible
                    sample_size = min(num_negatives, len(valid_indices))
                    neg_indices = random.sample(valid_indices, sample_size)
            
            # Add negative pairs
            for neg_idx in neg_indices:
                _add_pair(
                    i, neg_idx, center_item, items[neg_idx], center_item_data, df.iloc[neg_idx],
                    similarity_fn, noise_level, min_similarity, max_similarity,
                    center_words, context_words, labels, pair_types, 
                    center_values, context_values, value_col, "negative"
                )
    
    # Create output DataFrame
    pairs_data = {
        "center_word": center_words,
        "context_word": context_words,
        label_col: labels
    }
    
    if include_pair_type:
        pairs_data["pair_type"] = pair_types
        
    if include_attribute_values and value_col:
        pairs_data["center_value"] = center_values
        pairs_data["context_value"] = context_values
    
    pairs_df = pd.DataFrame(pairs_data)
    
    # Report statistics if requested
    if report_stats:
        _report_statistics(pairs_df, label_col)
    
    return pairs_df


def _add_pair(
    i: int, j: int, 
    center_item: Any, context_item: Any, 
    center_data: pd.Series, context_data: pd.Series,
    similarity_fn: Callable,
    noise_level: float,
    min_similarity: float, 
    max_similarity: float,
    center_words: List, 
    context_words: List, 
    labels: List,
    pair_types: List,
    center_values: List,
    context_values: List,
    value_col: Optional[str],
    pair_type: str
) -> None:
    """Helper function to add a pair to the output lists"""
    # Calculate similarity
    similarity = similarity_fn(center_data, context_data)
    
    # Apply more aggressive penalty for explicit negative examples
    if pair_type == "negative":
        similarity = similarity * 0.7  # Reduce similarity for negative examples
    
    # Add noise if specified
    if noise_level > 0:
        similarity = similarity + np.random.normal(0, noise_level)
        # Clamp to valid range
        similarity = max(min_similarity, min(max_similarity, similarity))
    
    # Add to output lists
    center_words.append(center_item)
    context_words.append(context_item)
    labels.append(similarity)
    pair_types.append(pair_type)
    
    # Add values if needed
    if value_col:
        center_values.append(center_data[value_col])
        context_values.append(context_data[value_col])


def _report_statistics(pairs_df: pd.DataFrame, label_col: str = "label") -> None:
    """Helper function to report statistics about the pairs"""
    total_pairs = len(pairs_df)
    print(f"Created {total_pairs} training pairs:")
    
    # If pair_type is available, report per type
    if "pair_type" in pairs_df.columns:
        for pair_type in sorted(pairs_df["pair_type"].unique()):
            type_df = pairs_df[pairs_df["pair_type"] == pair_type]
            print(f"  - {len(type_df)} {pair_type} pairs (avg similarity: {type_df[label_col].mean():.4f})")
    
    # Overall similarity stats
    print(f"\nSimilarity statistics:")
    print(f"  - Min: {pairs_df[label_col].min():.4f}")
    print(f"  - Max: {pairs_df[label_col].max():.4f}")
    print(f"  - Mean: {pairs_df[label_col].mean():.4f}")
    print(f"  - Median: {pairs_df[label_col].median():.4f}")
    
    # Print examples of highest and lowest similarity pairs
    print("\nHighest similarity pairs:")
    for _, row in pairs_df.nlargest(5, label_col).iterrows():
        print(f"  {row['center_word']} - {row['context_word']}: {row[label_col]:.4f}")
    
    print("\nLowest similarity pairs:")
    for _, row in pairs_df.nsmallest(5, label_col).iterrows():
        print(f"  {row['center_word']} - {row['context_word']}: {row[label_col]:.4f}")