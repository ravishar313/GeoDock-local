import sys
import biotite.structure.filter as filter_module

def patch_biotite():
    """Add filter_backbone function to biotite.structure"""
    if not hasattr(filter_module, 'filter_backbone'):
        # Create the filter_backbone function
        def filter_backbone(atom_array, **kwargs):
            """Filter backbone atoms using the correct biotite function"""
            return filter_module.filter_peptide_backbone(atom_array, **kwargs)
        
        # Add the function to the filter module
        filter_module.filter_backbone = filter_backbone
        
        # Also add it to the main biotite.structure module
        import biotite.structure
        if not hasattr(biotite.structure, 'filter_backbone'):
            biotite.structure.filter_backbone = filter_backbone
        
        print("Successfully patched biotite with filter_backbone function")
    else:
        print("filter_backbone already exists in biotite")

# Apply the patch immediately when this module is imported
patch_biotite()