# examples/data_generation_example.py
"""
Example showing how to generate training data for ValueVec models.
"""
import pandas as pd
import matplotlib.pyplot as plt
from training_data import create_color_spectrum_dataset, create_animal_dataset

def main():
    # Color spectrum dataset
    print("=" * 50)
    print("Creating color spectrum dataset")
    print("=" * 50)
    color_df, color_vocab = create_color_spectrum_dataset(n_colors=15)
    
    # Plot the color spectrum
    plt.figure(figsize=(12, 4))
    plt.scatter(color_df['estimated_value'], [1] * len(color_df), c='blue', s=100)
    
    # Add color labels
    for i, row in color_df.iterrows():
        plt.text(row['estimated_value'], 1.02, row['keyword'], 
                 horizontalalignment='center', fontsize=9)
    
    plt.yticks([])
    plt.xlabel('Wavelength (nm)')
    plt.title('Color Spectrum Visualization')
    plt.tight_layout()
    plt.savefig('color_spectrum.png')
    print("Saved color_spectrum.png")
    
    # Generate training pairs based on position in spectrum
    from training_data.data import create_color_training_pairs
    
    print("\nGenerating training pairs...")
    color_pairs = create_color_training_pairs(color_df)
    
    print("\nSample of color training pairs:")
    print(color_pairs.head())
    
    # Animal dataset example
    print("\n" + "=" * 50)
    print("Creating animal dataset")
    print("=" * 50)
    animal_df, animal_vocab = create_animal_dataset(n_animals=15)
    
    # Generate training pairs based on size
    from training_data.data import create_animal_training_pairs
    
    print("\nGenerating training pairs based on size...")
    size_pairs = create_animal_training_pairs(animal_df, primary_attribute='size')
    
    print("\nSample of animal training pairs (size-focused):")
    print(size_pairs.head())
    
    # Generate training pairs based on speed
    print("\nGenerating training pairs based on speed...")
    speed_pairs = create_animal_training_pairs(animal_df, primary_attribute='speed')
    
    print("\nSample of animal training pairs (speed-focused):")
    print(speed_pairs.head())

if __name__ == "__main__":
    main()