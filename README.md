# GeoDock Local Environment

This repository provides a complete [GeoDock](https://github.com/Graylab/GeoDock/tree/main) for local protein-protein docking.

## Quick Setup

### Prerequisites
- Python 3.12+
- CUDA 12.8 compatible GPU
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone and navigate to the repository:**
   ```bash
   git clone git@github.com:ravishar313/GeoDock-local.git
   cd geodock
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Download model weights:**
   The weights are already downloaded in the weights folder.

4. **Test the installation:**
   ```bash
   uv run python test_geodock_full.py
   ```
   
   **Note:** On first run, GeoDock will automatically download additional models from Hugging Face:
   - `esm2_t33_650M_UR50D.pt` (~2.5 GB) - ESM-2 language model for protein embeddings
   - `esm2_t33_650M_UR50D-contact-regression.pt` - Contact prediction model
   
   These will be cached in `~/.cache/torch/hub/checkpoints/` and only downloaded once.

## Dependencies

The project includes all necessary dependencies with GPU acceleration:

### Core Packages
- **PyTorch 2.8.0** with CUDA 12.8 support
- **torch-geometric 2.6.1** for graph neural networks
- **py3Dmol 2.5.2** for molecular visualization
- **geodock 1.0.4** for molecular docking
- **biotite 1.2.0** for structural bioinformatics

### Simplified Command Line Interface
- **run_geodock.py** - Easy-to-use CLI script with CPU fallback option
- Removed OpenMM/refinement dependencies for simpler, more reliable operation

### Torch-Geometric Extensions (CUDA-enabled)
- **torch-scatter 2.1.2+pt28cu128**
- **torch-sparse 0.6.18+pt28cu128**
- **torch-cluster 1.6.3+pt28cu128**
- **torch-spline-conv 1.2.2+pt28cu128**

## Usage

### Command Line Interface

Use the provided `run_geodock.py` script for easy molecular docking:

#### Basic Docking
```bash
uv run python run_geodock.py -p1 receptor.pdb -p2 ligand.pdb -o complex
```

#### Force CPU Mode
```bash
uv run python run_geodock.py -p1 receptor.pdb -p2 ligand.pdb -o complex --force-cpu
```

#### All Options
```bash
uv run python run_geodock.py --help
```

**Arguments:**
- `--protein1, -p1`: Path to receptor protein PDB file
- `--protein2, -p2`: Path to ligand protein PDB file  
- `--output, -o`: Output name for docked complex
- `--force-cpu, -cpu`: Force CPU mode even if GPU is available
- `--weights, -w`: Path to model weights (default: weights/dips_0.3.ckpt)

#### Example with 2OCJ.pdb
```bash
# Self-docking example (docks protein with itself)
uv run python run_geodock.py -p1 2OCJ.pdb -p2 2OCJ.pdb -o 2OCJ_self_dock
```

### Python API

For programmatic usage, you can use the GeoDock Python API directly:

```python
# Import the compatibility patch
import biotite_patch

# Initialize GeoDock
from geodock.GeoDockRunner import GeoDockRunner
geodock = GeoDockRunner(ckpt_file="weights/dips_0.3.ckpt")

# Run molecular docking
result = geodock.dock(
    partner1="receptor.pdb",
    partner2="ligand.pdb", 
    out_name="complex"
)
```


## Configuration

### Project Structure
```
geodock/
├── pyproject.toml          # Project configuration
├── run_geodock.py         # Command-line interface script
├── weights/
│   └── dips_0.3.ckpt      # Model weights (49.4 MB)
├── biotite_patch.py       # Compatibility patch
├── test_geodock_full.py   # Installation test
├── .venv/                 # Virtual environment
└── README.md              # This file
```

### Customization
- Edit `pyproject.toml` to modify dependencies
- Model weights can be updated by replacing `weights/dips_0.3.ckpt`
- CUDA version can be adjusted in wheel URLs for different GPU configurations

## Testing

Run the comprehensive test to verify the installation:
```bash
uv run python test_geodock_full.py
```

This test will:
- Verify all package imports
- Check CUDA availability
- Test model weights loading
- Validate GeoDock functionality

## Troubleshooting

### Common Issues

1. **CUDA version mismatch**: Ensure your GPU driver supports CUDA 12.8
2. **Import errors**: Make sure to `import biotite_patch` before using GeoDock

### Memory Issues
- **Force CPU mode**: Use `--force-cpu` flag for large proteins that exceed GPU memory
- **Recommended**: Always test with `--force-cpu` first for new proteins
- **CPU performance**: Docking still works efficiently on CPU, just takes longer

### Compatibility Notes
- The `biotite_patch.py` file provides compatibility between biotite 1.2.0 and ESM package
- All torch-geometric packages are built with CUDA 12.8 optimization
- Python 3.12+ is required for compatibility
- OpenMM refinement NOT included as of now

## TODO
- [ ] Add OpenMM refinement

## Acknowledgments
The code is adapted from the original GeoDock repository [here](https://github.com/Graylab/GeoDock)

## 📄 License

This setup follows the license terms of the original GeoDock project and its dependencies.