import argparse
import os
import sys
import torch


def force_cpu_mode():
    """Force PyTorch to use CPU mode"""
    original_is_available = torch.cuda.is_available
    
    def cpu_only():
        return False
    
    torch.cuda.is_available = cpu_only
    print("Forced CPU mode to avoid GPU memory issues")
    return original_is_available


def main():
    parser = argparse.ArgumentParser(
        description="Run GeoDock molecular docking simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_geodock.py -p1 receptor.pdb -p2 ligand.pdb -o complex
  python run_geodock.py -p1 receptor.pdb -p2 ligand.pdb -o complex --force-cpu
        """
    )
    
    parser.add_argument(
        '--protein1', '-p1',
        required=True,
        help='Path to the first protein PDB file (receptor)'
    )
    
    parser.add_argument(
        '--protein2', '-p2',
        required=True,
        help='Path to the second protein PDB file (ligand)'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output name for the docked complex'
    )
    
    parser.add_argument(
        '--force-cpu', '-cpu',
        action='store_true',
        help='Force CPU mode even if GPU is available'
    )
    
    parser.add_argument(
        '--weights', '-w',
        default='weights/dips_0.3.ckpt',
        help='Path to model weights (default: weights/dips_0.3.ckpt)'
    )
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.protein1):
        print(f"Error: Protein 1 file not found: {args.protein1}")
        sys.exit(1)
    
    if not os.path.exists(args.protein2):
        print(f"Error: Protein 2 file not found: {args.protein2}")
        sys.exit(1)
    
    if not os.path.exists(args.weights):
        print(f"Error: Weights file not found: {args.weights}")
        print("Download weights with:")
        print("  mkdir -p weights")
        print("  wget https://raw.githubusercontent.com/Graylab/GeoDock/main/geodock/weights/dips_0.3.ckpt -O weights/dips_0.3.ckpt")
        sys.exit(1)
    
    # Force CPU mode if requested
    if args.force_cpu:
        force_cpu_mode()
    
    # Import biotite patch first
    try:
        import biotite_patch
        print("Applied biotite compatibility patch")
    except ImportError:
        print("Error: biotite_patch.py not found")
        sys.exit(1)
    
    # Import GeoDock
    try:
        from geodock.GeoDockRunner import GeoDockRunner
        print("Imported GeoDockRunner")
    except ImportError as e:
        print(f"Error importing GeoDock: {e}")
        print("Make sure all dependencies are installed with: uv sync")
        sys.exit(1)
    
    # Print configuration
    print("\n" + "="*50)
    print("GeoDock Configuration")
    print("="*50)
    print(f"Protein 1 (Receptor): {args.protein1}")
    print(f"Protein 2 (Ligand):   {args.protein2}")
    print(f"Output:               {args.output}")
    print(f"Force CPU:            {args.force_cpu}")
    print(f"Weights:              {args.weights}")
    
    # Show device info
    if torch.cuda.is_available():
        print(f"Device:               CUDA ({torch.cuda.get_device_name()})")
    else:
        print("Device:               CPU")
    print("="*50)
    
    # Initialize GeoDock
    try:
        print("Initializing GeoDockRunner...")
        geodock = GeoDockRunner(ckpt_file=args.weights)
        print("GeoDockRunner initialized successfully")
    except Exception as e:
        print(f"Error initializing GeoDockRunner: {e}")
        sys.exit(1)
    
    # Run docking
    try:
        print("Starting molecular docking...")
        print("   This may take several minutes depending on protein size...")
        
        result = geodock.dock(
            partner1=args.protein1,
            partner2=args.protein2,
            out_name=args.output
        )
        
        print("Docking completed successfully!")
        print(f"Results saved with prefix: {args.output}")
        
        # List output files
        output_files = [
            f"{args.output}.pdb",
            f"{args.output}_scores.txt",
            f"{args.output}_poses.txt"
        ]
        
        print("\nGenerated files:")
        for file in output_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f" {file} ({size} bytes)")
            else:
                print(f" {file} (not found)")
        
        return 0
        
    except Exception as e:
        print(f"Error during docking: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())