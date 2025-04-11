# ValueVec ![MIT License](https://img.shields.io/badge/license-MIT-green) ![PyPI](https://img.shields.io/pypi/v/valuevec) ![Python](https://img.shields.io/pypi/pyversions/valuevec)

**ValueVec** is a framework for learning word embeddings driven by external continuous values, such as similarity labels based on behavior, attributes, or measurements. Unlike traditional word2vec models that rely solely on linguistic context, ValueVec uses numeric supervision to capture more targeted relationships between terms.

---

## Architecture Overview

ValueVec supports two training paradigms:

| Model         | Description                                                 | Use Case                    |
| ------------- | ----------------------------------------------------------- | --------------------------- |
| manual_model/ | Custom update logic based on cosine gradient approximations | For learning & debugging    |
| nn_model/     | PyTorch-based training using nn.Embedding + MSE loss        | For real-world applications |

> Detailed explanation available in [`docs/architecture.md`](docs/architecture.md)

---

## Key Features

- **Continuous Supervision**: Uses numeric similarity scores between words.
- **Cosine-Based Optimization**: Directly optimizes cosine similarity between embeddings.
- **Manual + Neural Versions**: Choose between interpretability or performance.
- **Custom Datasets**: Generate value-supervised datasets from colors, fruits, animals, etc.
- **Visualizable**: Easily inspect the embedding space with built-in PCA projection.

---

## Installation

```bash
# Option 1: From PyPI
pip install valuevec

# Option 2: From source
git clone https://github.com/rdoku/valuevec.git
cd valuevec
pip install -e .
```

## Quick Start

```bash
# Use an example script to train a value-driven embedding model
python examples/basic_usage.py
```

For custom training data, see `docs/usage.md`.

## Example Applications

- **E-commerce** – Group keywords with similar price influence
- **Finance** – Cluster terms by correlation with financial metrics
- **Customer Modeling** – Link descriptors to user value or conversion likelihood
- **Sentiment Analysis** – Model emotional intensity beyond polarity

## Project Layout

```bash
valuevec/
├── manual_model/    # Manual gradient updates
├── nn_model/        # PyTorch-based implementation
├── training_data/   # Data generation utilities
├── examples/        # Ready-to-run training and analysis
├── tests/           # Unit tests
├── docs/            # Markdown documentation
```

## Documentation

- `docs/architecture.md` – Neural vs. manual training
- `docs/usage.md` – Training, inference, visualization
- `docs/CONTRIBUTING.md` – Guidelines for contributing

## Contributing

We welcome contributions! Get started with:

```bash
git checkout -b feature/your-feature
```

Then open a Pull Request. For details, see `docs/CONTRIBUTING.md`.

## License

MIT License. See the LICENSE file for details.

## Citation

If you use ValueVec in your work, please cite it as:

```
@software{valuevec2025,
  author = {Ronald Doku},
  title = {ValueVec: Value-Driven Word Embeddings},
  year = {2025},
  url = {https://github.com/rdoku/valuevec}
}
```
