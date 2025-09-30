# GeoDock Repository Documentation

## Repository Description and Purpose

GeoDock is a deep learning-based tool for protein-protein docking. This repository provides a complete local environment setup for running GeoDock molecular docking predictions. The tool predicts the 3D structure of protein-protein complexes by computationally docking two input protein structures together.

GeoDock uses graph neural networks (GNN) and protein language models (ESM-2) to predict favorable binding poses between two protein partners. The repository is adapted from the original [GeoDock by Graylab](https://github.com/Graylab/GeoDock) and includes all necessary dependencies with GPU acceleration support.

**Key Features:**
- Protein-protein docking using deep learning
- Support for both GPU (CUDA 12.8) and CPU execution
- Automatic downloading of ESM-2 protein embedding models
- Simplified command-line interface for easy usage
- Python API for programmatic access

## Installation Requirements

### System Prerequisites
- **Python**: 3.12 or higher
- **GPU** (Optional): 
  - CUDA 12.8 compatible GPU with **16GB+ VRAM** recommended for GPU mode
  - **Tested configurations**:
    - RTX 4070 (11.56 GB VRAM): ❌ Out-of-memory errors with typical proteins
    - CPU mode: ✅ Reliable for all protein sizes
  - **Recommendation**: Use CPU mode as default (reliable and reasonably fast)
- **RAM**: 8GB+ recommended for CPU mode
- **Package Manager**: [uv](https://docs.astral.sh/uv/) package manager
- **Operating System**: Linux (tested on Linux 6.8.0)

### Python Dependencies
The repository includes the following core packages:

- **PyTorch 2.8.0** - Deep learning framework with CUDA 12.8 support
- **torch-geometric 2.6.1** - Graph neural network library
- **geodock 1.0.4** - Core molecular docking package
- **biotite 1.2.0** - Structural bioinformatics toolkit
- **py3Dmol 2.5.2** - Molecular visualization (optional)

### Torch-Geometric Extensions (CUDA-enabled)
- **torch-scatter 2.1.2+pt28cu128**
- **torch-sparse 0.6.18+pt28cu128**
- **torch-cluster 1.6.3+pt28cu128**
- **torch-spline-conv 1.2.2+pt28cu128**

## Installation Instructions

### Step 1: Clone the Repository
```bash
git clone git@github.com:ravishar313/GeoDock-local.git
cd geodock
```

### Step 2: Install Dependencies
```bash
uv sync
```

This command will install all required Python packages including PyTorch with CUDA support and all torch-geometric extensions.

### Step 3: Model Weights

#### Primary Model Weights (dips_0.3.ckpt)
The main GeoDock model weights are already included in the `weights/` folder:
- **File**: `weights/dips_0.3.ckpt`
- **Size**: 50 MB
- **Description**: Pre-trained GeoDock model trained on DIPS dataset

If the weights file is missing, download it manually:
```bash
mkdir -p weights
wget https://raw.githubusercontent.com/Graylab/GeoDock/main/geodock/weights/dips_0.3.ckpt -O weights/dips_0.3.ckpt
```

#### Additional Model Weights (Automatic Download)
On the first run, GeoDock will automatically download ESM-2 protein language models from Hugging Face. These are used for generating protein embeddings:

1. **esm2_t33_650M_UR50D.pt** (~2.5 GB)
   - ESM-2 language model for protein embeddings
   
2. **esm2_t33_650M_UR50D-contact-regression.pt**
   - Contact prediction model

**Cache Location**: `~/.cache/torch/hub/checkpoints/`

These models are downloaded once and cached for future use.

### Step 4: Test Installation
Verify the installation by running the test script:
```bash
uv run python test_geodock_full.py
```

The test will verify:
- All package imports
- CUDA availability (if GPU present)
- Model weights loading
- GeoDock functionality

## Usage Instructions

### Command Line Interface

The repository provides a simplified CLI through `run_geodock.py` script.

#### Basic Usage Syntax
```bash
uv run python run_geodock.py -p1 <protein1.pdb> -p2 <protein2.pdb> -o <output_name>
```

#### Example: Basic Docking (Recommended with CPU)
```bash
uv run python run_geodock.py -p1 protein1.pdb -p2 protein2.pdb -o complex --force-cpu
```

#### Example: Self-Docking with Provided Example
The repository includes an example PDB file `2OCJ.pdb` (1526 lines). You can use it for testing:
```bash
uv run python run_geodock.py -p1 2OCJ.pdb -p2 2OCJ.pdb -o 2OCJ_self_dock
```

#### Example: GPU Mode (Requires 16GB+ VRAM)
Only use GPU mode if you have sufficient GPU memory:
```bash
uv run python run_geodock.py -p1 protein1.pdb -p2 protein2.pdb -o complex
```

**Warning**: GPU mode may fail with out-of-memory errors even on GPUs with 11+ GB VRAM. CPU mode is recommended for reliability.

### Usage Arguments

| Argument | Short Form | Required | Default | Description |
|----------|------------|----------|---------|-------------|
| `--protein1` | `-p1` | Yes | - | Path to the first protein PDB file (binding partner 1) |
| `--protein2` | `-p2` | Yes | - | Path to the second protein PDB file (binding partner 2) |
| `--output` | `-o` | Yes | - | Output name prefix for docked complex |
| `--force-cpu` | `-cpu` | No | False | Force CPU mode (recommended for reliability) |
| `--weights` | `-w` | No | `weights/dips_0.3.ckpt` | Path to model weights file |

### Python API Usage

For programmatic usage in Python scripts:

```python
# Import the compatibility patch (REQUIRED)
import biotite_patch

# Initialize GeoDock
from geodock.GeoDockRunner import GeoDockRunner
geodock = GeoDockRunner(ckpt_file="weights/dips_0.3.ckpt")

# Run molecular docking
result = geodock.dock(
    partner1="protein1.pdb",
    partner2="protein2.pdb", 
    out_name="complex"
)
```

**Important**: The `biotite_patch` module must be imported before using GeoDock to ensure compatibility between biotite 1.2.0 and the ESM package.

## Input Files and Format

### Input File Requirements

GeoDock accepts protein structures in **PDB format** (Protein Data Bank format).

#### PDB File Format
- **Format**: Standard PDB text format
- **Extension**: `.pdb`
- **Content**: Atomic coordinates of protein structures
- **Chains**: Can contain single or multiple chains

#### PDB File Structure Example
```
CRYST1   68.913   69.364   84.179  90.00  90.11  90.00 P 1 21 1      1
ATOM      1  N   SER A  96      13.651 -16.577  32.202  1.00 46.57           N  
ATOM      2  CA  SER A  96      12.392 -17.077  32.829  1.00 45.90           C  
ATOM      3  C   SER A  96      11.238 -16.133  32.479  1.00 44.81           C  
ATOM      4  O   SER A  96      11.239 -15.515  31.411  1.00 45.24           O  
ATOM      5  CB  SER A  96      12.571 -17.161  34.350  1.00 47.65           C  
...
```

### Example Input File

The repository includes an example PDB file:

**File**: `2OCJ.pdb`
**Download Link**: Available in repository at `https://github.com/ravishar313/GeoDock-local/blob/main/2OCJ.pdb`

To download directly:
```bash
wget https://raw.githubusercontent.com/ravishar313/GeoDock-local/main/2OCJ.pdb
```

### Input Requirements
- Both protein partners must be in valid PDB format
- Files must exist and be readable
- The tool can dock a protein with itself (self-docking)
- No specific size limitations, but GPU memory constraints may apply for very large proteins

## Output Files and Format

GeoDock generates multiple output files with information about the docking results:

### Output File Types

#### 1. Docked Complex PDB File
- **Filename**: `{output_name}_docked.pdb` or `{output_name}.pdb`
- **Format**: Standard PDB format
- **Content**: 3D coordinates of the docked protein complex
- **Description**: Contains the predicted binding pose with both protein partners in their docked orientation

Example output from `2OCJ_self_dock`:
```
ATOM      1  N   SER A  96      13.651 -16.577  32.202  1.00 46.57           N  
ATOM      2  CA  SER A  96      12.392 -17.077  32.829  1.00 45.90           C  
...
```

#### 2. Scores File (Expected)
- **Filename**: `{output_name}_scores.txt`
- **Format**: Text file
- **Content**: Docking scores and confidence metrics
- **Description**: Contains scoring information for the predicted docking poses

#### 3. Poses File (Expected)
- **Filename**: `{output_name}_poses.txt`
- **Format**: Text file
- **Content**: Information about different docking poses
- **Description**: May contain multiple predicted poses with their corresponding scores

**Note**: The exact format of `_scores.txt` and `_poses.txt` files depends on the GeoDock package implementation. The CLI script checks for these files after docking completion.

### Output File Locations
All output files are saved in the current working directory with the specified output name prefix.

## Error Messages and Their Meaning

### Common Error Messages

#### 1. Input File Not Found
```
Error: Protein 1 file not found: {filename}
```
**Meaning**: The specified receptor PDB file does not exist
**Solution**: Verify the file path and ensure the file exists

```
Error: Protein 2 file not found: {filename}
```
**Meaning**: The specified second protein PDB file does not exist
**Solution**: Verify the file path and ensure the file exists

#### 2. Weights File Missing
```
Error: Weights file not found: {weights_path}
Download weights with:
  mkdir -p weights
  wget https://raw.githubusercontent.com/Graylab/GeoDock/main/geodock/weights/dips_0.3.ckpt -O weights/dips_0.3.ckpt
```
**Meaning**: The model weights file is not in the expected location
**Solution**: Download the weights using the provided wget command

#### 3. Biotite Patch Missing
```
Error: biotite_patch.py not found
```
**Meaning**: The compatibility patch file is missing from the repository
**Solution**: Ensure `biotite_patch.py` is present in the root directory

#### 4. Import Error
```
Error importing GeoDock: {error_details}
Make sure all dependencies are installed with: uv sync
```
**Meaning**: GeoDock package or its dependencies are not properly installed
**Solution**: Run `uv sync` to install all required packages

#### 5. Initialization Error
```
Error initializing GeoDockRunner: {error_details}
```
**Meaning**: Failed to initialize the GeoDock model
**Solution**: Check that weights file is valid and all dependencies are installed

#### 6. Docking Error
```
Error during docking: {error_details}
```
**Meaning**: An error occurred during the docking process
**Solution**: Check input files are valid PDB format, try CPU mode with `--force-cpu`, or verify sufficient memory is available

## Known Issues and Solutions

### Issue 1: CUDA Out of Memory
**Symptom**: GPU memory exhausted during docking, even on GPUs with 11+ GB VRAM
```
CUDA out of memory. Tried to allocate 74.00 MiB. GPU 0 has a total capacity of 11.56 GiB...
torch.OutOfMemoryError: CUDA out of memory...
```

**Explanation**: 
- GeoDock's memory requirements can exceed 11 GB VRAM for typical proteins
- Even proteins like 2OCJ (1526 lines) fail on RTX 4070 (11.56 GB)
- GPU with 16GB+ VRAM recommended, or use CPU mode

**Solution**: 
- **Recommended**: Always use the `--force-cpu` flag for reliable operation
- CPU mode completes successfully and runs reasonably fast (~6-7 seconds for typical proteins)
- Embedding takes ~0.7 seconds on CPU vs ~0.2 seconds on GPU

```bash
uv run python run_geodock.py -p1 protein1.pdb -p2 protein2.pdb -o result --force-cpu
```

**Real-world example** (2OCJ.pdb self-docking):
- **GPU (RTX 4070, 11.56 GB)**: Failed with out-of-memory error
- **CPU**: Completed successfully in 6.58 seconds (embedding: 0.71s)

### Issue 2: CUDA Version Mismatch
**Symptom**: CUDA-related errors or GPU not being detected
**Solution**: 
- Ensure GPU driver supports CUDA 12.8
- Check CUDA version: `nvidia-smi`
- May need to update GPU drivers

### Issue 3: biotite Compatibility
**Symptom**: Import errors related to `filter_backbone` function
**Solution**: 
- The repository includes `biotite_patch.py` that automatically fixes this
- Always import `biotite_patch` before using GeoDock
- The patch adds the missing `filter_backbone` function to biotite 1.2.0

### Issue 4: First Run Takes Long Time
**Symptom**: First execution takes several minutes to start
**Solution**: 
- This is normal behavior - GeoDock downloads ESM-2 models (~2.5 GB) on first run
- Models are cached in `~/.cache/torch/hub/checkpoints/`
- Subsequent runs will be much faster

### Issue 5: Import Errors After Installation
**Symptom**: Packages cannot be imported despite successful `uv sync`
**Solution**: 
- Make sure to use `uv run python` prefix for all commands
- This ensures the virtual environment is activated
- Alternatively, activate the venv manually: `source .venv/bin/activate`

### Issue 6: OpenMM Refinement Warning
**Symptom**: Warning message after successful docking
```
OpenMM not installed. Please install OpenMM to use refinement.
```
**Explanation**: 
- OpenMM is used for optional structure refinement after docking
- This is a warning, not an error - docking completes successfully without it
- The repository intentionally excludes OpenMM for simpler setup

**Solution**: 
- This warning can be safely ignored
- The docked structure is produced successfully without refinement
- If refinement is needed, OpenMM can be installed separately

### Issue 7: Deprecation Warnings
**Symptom**: Warning about torch.cross during execution
```
UserWarning: Using torch.cross without specifying the dim arg is deprecated.
```
**Explanation**: 
- This is a deprecation warning from the GeoDock package code
- Does not affect functionality or results

**Solution**: 
- This warning can be safely ignored
- It will be fixed in future versions of the GeoDock package

## Additional Configuration Notes

### Biotite Compatibility Patch
The repository includes `biotite_patch.py` that provides compatibility between biotite 1.2.0 and the ESM package. This patch:
- Adds the `filter_backbone` function to biotite.structure
- Maps to the correct `filter_peptide_backbone` function
- Must be imported before using GeoDock

### Project Structure
```
geodock/
├── pyproject.toml          # Project configuration and dependencies
├── run_geodock.py          # Command-line interface script
├── weights/
│   └── dips_0.3.ckpt       # Model weights (50 MB)
├── biotite_patch.py        # Compatibility patch for biotite
├── test_geodock_full.py    # Installation test script
├── 2OCJ.pdb                # Example protein structure file
├── .venv/                  # Virtual environment (created by uv)
├── uv.lock                 # Dependency lock file
└── README.md               # Repository documentation
```

### Device Selection
- GeoDock automatically detects and uses GPU if available
- To check device being used, look for the configuration output:
  ```
  Device:               CUDA (NVIDIA GeForce RTX 3090)
  ```
  or
  ```
  Device:               CPU
  ```

### Performance Considerations
- **GPU Mode**: 
  - Requires 16GB+ VRAM for reliable operation
  - May fail on GPUs with 11GB VRAM even for typical proteins
  - Embedding is faster (~0.2s vs ~0.7s on CPU)
  - Not recommended unless you have high-end GPU
  
- **CPU Mode** (Recommended): 
  - Reliable and works for all protein sizes
  - Reasonably fast (~6-7 seconds for typical proteins like 2OCJ)
  - No memory limitations
  - Embedding takes ~0.7 seconds
  
- **Recommended Workflow**: Always use `--force-cpu` for production use

### Performance Benchmarks (2OCJ.pdb Self-Docking)
- **CPU Mode**:
  - Embedding: 0.71 seconds
  - Total docking: 6.58 seconds
  - Status: ✓ Completed successfully
  
- **GPU Mode (RTX 4070, 11.56 GB VRAM)**:
  - Embedding: 0.22 seconds
  - Total docking: Failed with CUDA out-of-memory error
  - Status: ✗ Failed

## Limitations

### Current Limitations
1. **No Refinement**: OpenMM refinement is not included in this version
2. **Training Not Supported**: This repository is configured only for inference/prediction
3. **PDB Format Only**: Only accepts PDB format input files
4. **CUDA 12.8**: Torch-geometric extensions are built specifically for CUDA 12.8
5. **GPU Memory Requirements**: Requires 16GB+ VRAM for GPU mode; CPU mode recommended for most use cases

### Not Included
- Training scripts or training data
- Model retraining functionality
- OpenMM-based structure refinement
- Support for other structure formats (e.g., mmCIF, MOL2)

## Example Workflow

### Complete Example: Running Docking from Scratch

```bash
# 1. Navigate to repository
cd geodock

# 2. Ensure dependencies are installed
uv sync

# 3. Test installation
uv run python test_geodock_full.py

# 4. Run docking with CPU mode (recommended)
uv run python run_geodock.py -p1 2OCJ.pdb -p2 2OCJ.pdb -o test_output --force-cpu

# 5. (Optional) Try GPU mode if you have 16GB+ VRAM
# Warning: May fail with out-of-memory error on GPUs with <16GB VRAM
# uv run python run_geodock.py -p1 2OCJ.pdb -p2 2OCJ.pdb -o test_output_gpu

# 6. Check output files
ls -lh test_output*
```

Expected output:
```
test_output.pdb          # Docked complex structure
```

**Note**: Additional files like `_scores.txt` and `_poses.txt` may or may not be generated depending on the GeoDock package version.

### Expected Console Output (Successful Run)
```
Forced CPU mode to avoid GPU memory issues
Successfully patched biotite with filter_backbone function
Applied biotite compatibility patch
Imported GeoDockRunner

==================================================
GeoDock Configuration
==================================================
Protein 1 (Receptor): 2OCJ.pdb
Protein 2 (Ligand):   2OCJ.pdb
Output:               complex
Force CPU:            True
Weights:              weights/dips_0.3.ckpt
Device:               CPU
==================================================
Initializing GeoDockRunner...
GeoDockRunner initialized successfully
Starting molecular docking...
   This may take several minutes depending on protein size...
Completed embedding in 0.71 seconds.
Completed docking in 6.58 seconds.
OpenMM not installed. Please install OpenMM to use refinement.
```

## References

- **Original GeoDock Repository**: https://github.com/Graylab/GeoDock
- **PyTorch**: https://pytorch.org/
- **PyTorch Geometric**: https://pytorch-geometric.readthedocs.io/
- **ESM (Evolutionary Scale Modeling)**: Protein language models by Meta AI
- **Biotite**: https://www.biotite-python.org/
- **UV Package Manager**: https://docs.astral.sh/uv/
