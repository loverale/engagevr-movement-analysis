import os
import re
from pathlib import Path
import zipfile
import logging
import tempfile
from bids import * # bad practice, in debugging mode
from ungage import *
import pandas as pd
from dddp import semantics_angles_unity, semantics_axes_unity, set_dddp_semantics, get_dddp_semantics


def process_myrec_files():
    """Process all .myrec files in the given directory."""
    raw_files_dir = "./raw_files"  # Define the directory path
    sub_folders_path = list(Path(raw_files_dir).rglob("*.myrec"))  # Get list of all .myrec files
    
    if not sub_folders_path:
        print(f"No .myrec files found in {raw_files_dir}.")
        return

    for myrec_file in sub_folders_path:
        myrec_file = str(myrec_file)  # Convert Path object to string
        newfolder = os.path.splitext(os.path.basename(myrec_file))[0]  # Remove .myrec extension
        newfolder_path = os.path.join("./processed_files", newfolder)
        
        os.makedirs(newfolder_path, exist_ok=True)
        
        bd = bids(newfolder_path, readonly=False)
        player_names = myrec_player_names(myrec_file)
        
        # Clean player names
        player_names = {name: re.sub(r'[^a-zA-Z0-9]', '', name) for name in player_names}
        
        myrec_to_bids(myrec_file, bd, "sessionstring", "taskstring", player_names)
    
    print("Processing complete.")

process_myrec_files()