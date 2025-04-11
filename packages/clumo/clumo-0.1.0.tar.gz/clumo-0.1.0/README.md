# CluMo: Clustering-based Motif Discovery

CluMo is a Python package for discovering DNA motifs from deep learning models using clustering approaches. It uses feature attribution techniques to identify important regions in DNA sequences and clusters them to find common motifs.

## Installation

```bash
pip install clumo
```

## Quick Start

```python
import torch
from clumo import CluMo
import pandas as pd

# Load your torch model
model = TheModelClass(*args, **kwargs)
model.load_state_dict(torch.load(PATH, weights_only=True))

# Initialize CluMo with the model
clumo = CluMo(model=model, output_dir="results")

# Prepare your sequence data, "efficiency" can be other targeted sequence properties
df = pd.DataFrame({
    "sequence": ["ATCGATCG", "GCTAGCTA", ...],
    "label": [1, 0, ...],
    "efficiency": [0.8, 0.2, ...]
})
motifs = clumo.analyze_from_dataframe(df, seq_col="sequence", label_col="label", eff_col="efficiency")

```

## Features

- Discover DNA motifs using deep learning feature attribution
- Clustering approach to identify common motifs
- Statistical significance testing for motif enrichment
- Visualization of motifs as sequence logos

## Requirements

- Python 3.9
- PyTorch
- Captum
- NumPy
- Pandas
- Matplotlib
- logomaker
- scikit-learn
- SciPy

## Citation

Please use the following to cite our work:

```bibtex
@article{gimpel2024deep,
  title={Deep learning uncovers sequence-specific amplification bias in multi-template PCR},
  author={Gimpel, Andreas L and Fan, Bowen and Chen, Dexiong and W{\"o}lfle, Laetitia OD and Horn, Max and Meng-Papaxanthos, Laetitia and Antkowiak, Philipp L and Stark, Wendelin J and Christen, Beat and Borgwardt, Karsten and others},
  journal={bioRxiv},
  pages={2024--09},
  year={2024},
  publisher={Cold Spring Harbor Laboratory}
}
```