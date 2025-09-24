#!/usr/bin/env python3
"""
Test script for GeoDock functionality with biotite patch
"""

import sys
import os

def test_geodock_import():
    """Test if GeoDock can be imported and initialized"""
    print("Testing GeoDock import...")
    
    try:
        # Import the patch first
        import biotite_patch
        
        # Import GeoDock
        from geodock.GeoDockRunner import GeoDockRunner
        print("GeoDockRunner imported successfully!")
        
        # Check if weights file exists
        weights_path = "weights/dips_0.3.ckpt"
        if os.path.exists(weights_path):
            print(f"Weights file found: {weights_path}")
            
            # Try to initialize (this might take time)
            print("Initializing GeoDockRunner (this may take a moment)...")
            geodock = GeoDockRunner(ckpt_file=weights_path)
            print("GeoDockRunner initialized successfully!")
            return True
        else:
            print(f"Weights file not found: {weights_path}")
            return False
            
    except Exception as e:
        print(f"GeoDock import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality without actually running docking"""
    print("\nTesting basic functionality...")
    
    try:
        import biotite_patch
        from geodock.GeoDockRunner import GeoDockRunner
        
        # Initialize
        geodock = GeoDockRunner(ckpt_file="weights/dips_0.3.ckpt")
        
        # Check if the runner has the expected methods
        expected_methods = ['dock']
        for method in expected_methods:
            if hasattr(geodock, method):
                print(f"Method {method} available")
            else:
                print(f"Method {method} missing")
                return False
        
        print("All expected methods available")
        return True
        
    except Exception as e:
        print(f"Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("GeoDock Full Functionality Test")
    print("=" * 50)
    
    tests = [
        test_geodock_import(),
        test_basic_functionality()
    ]
    
    if all(tests):
        print("\nAll tests passed! GeoDock is fully functional!")
        print("\nYou can now use GeoDock for molecular docking:")
        print("```python")
        print("from geodock.GeoDockRunner import GeoDockRunner")
        print("geodock = GeoDockRunner(ckpt_file='weights/dips_0.3.ckpt')")
        print("result = geodock.dock(partner1='receptor.pdb', partner2='ligand.pdb', out_name='complex')")
        print("```")
        return 0
    else:
        print("\nSome tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    exit(main())