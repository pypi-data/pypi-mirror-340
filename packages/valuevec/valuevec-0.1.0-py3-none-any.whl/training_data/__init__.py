# valuevec/training_data/__init__.py

# Import key functions from this package
from .data import create_color_spectrum_dataset, create_animal_dataset
from .training_pairs import create_training_pairs

__all__ = [
    "create_training_pairs",
    "create_color_spectrum_dataset",
    "create_animal_dataset"
]