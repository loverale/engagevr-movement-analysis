import os
import json
import zipfile
import logging
import tempfile
import pandas as pd
from pathlib import Path
from bids import bids_write_motion_files
from dddp import semantics_angles_unity, semantics_axes_unity, set_dddp_semantics, get_dddp_semantics

# all credit for this goes to @markromanmiller, this file is simply a Python version of the following public Github in R:
# https://github.com/markromanmiller/ungage

def check_file(myrec_path):
    """Check if the given .myrec file exists and is a valid file."""
    if not os.path.exists(myrec_path):
        raise FileNotFoundError(f"Could not find file `{myrec_path}` from working directory `{os.getcwd()}`.")
    if os.path.isdir(myrec_path):
        raise IsADirectoryError(f"Expected a file but got a directory: `{myrec_path}`.")
    return os.path.abspath(myrec_path)

def unzip_myrec(absolute_path_to_myrec, unzip_dest):
    """Unzip .myrec file to the given destination."""
    logging.info("Unzipping myrec file...")
    with zipfile.ZipFile(absolute_path_to_myrec, 'r') as zip_ref:
        zip_ref.extractall(unzip_dest)
    
    file_list = os.listdir(unzip_dest)
    logging.info(f"Unzipping {sum(f.startswith('stream') for f in file_list)} stream files...")
    
    for file in file_list:
        if file != "count.txt" and zipfile.is_zipfile(os.path.join(unzip_dest, file)):
            with zipfile.ZipFile(os.path.join(unzip_dest, file), 'r') as inner_zip:
                inner_zip.extractall(os.path.join(unzip_dest, f"{file}_dir"))
    logging.info("Streams unzipped.")

def get_player_names(master_json):
    """Extract player names from master JSON safely."""
    if "avatar_variables_v1" not in master_json and "avatar_variables" not in master_json:
        raise KeyError("Neither 'avatar_variables_v1' nor 'avatar_variables' found in master JSON.")

    # Debugging: Check the type and structure of `avatar_variables_v1`
    if "avatar_variables_v1" in master_json:
        print(f"avatar_variables_v1 type: {type(master_json['avatar_variables_v1'])}")
        print(f"avatar_variables_v1 content preview: {master_json['avatar_variables_v1'][:3] if isinstance(master_json['avatar_variables_v1'], list) else master_json['avatar_variables_v1']}")

    # Ensure the data structure is correct before iterating
    if isinstance(master_json.get("avatar_variables_v1"), list):
        return [player["name"] for player in master_json["avatar_variables_v1"] if isinstance(player, dict) and "name" in player]

    if isinstance(master_json.get("avatar_variables"), list):
        return [player["avatarVars"]["name"] for player in master_json["avatar_variables"] if isinstance(player, dict) and "avatarVars" in player and "name" in player["avatarVars"]]

    raise TypeError("Expected 'avatar_variables_v1' or 'avatar_variables' to be a list of dictionaries.")
    
def myrec_player_names(myrec_path):
    """Extract player names from a .myrec file."""
    absolute_path_to_myrec = check_file(myrec_path)

    with tempfile.TemporaryDirectory() as unzip_dest:
        logging.debug(f"Working at {unzip_dest}")
        unzip_myrec(absolute_path_to_myrec, unzip_dest)
        
        master_json_path = os.path.join(unzip_dest, "master_dir", "master.txt")
        
        if not os.path.exists(master_json_path):
            raise FileNotFoundError(f"Expected master JSON file not found: {master_json_path}")
        
        # Ensure JSON is loaded correctly
        with open(master_json_path, "r", encoding="utf-8") as f:
            file_content = f.read().strip()  # Read as string
            try:
                master_json = json.loads(file_content)  # Parse JSON manually
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON in {master_json_path}: {e}")
        
        # Debugging output
        print(f"Master JSON type: {type(master_json)}")
        print(f"Master JSON content: {file_content[:500] if isinstance(file_content, str) else json.dumps(master_json, indent=2)}")

        if not isinstance(master_json, dict):
            raise TypeError(f"Expected JSON dictionary but got {type(master_json)} in {master_json_path}")
        
        print(f"JSON Keys: {master_json.keys()}")

        if "avatar_variables_v1" not in master_json and "avatar_variables" not in master_json:
            raise KeyError(f"Neither 'avatar_variables_v1' nor 'avatar_variables' found in {master_json_path}")
        
        return get_player_names(master_json)  # Now master_json is safely parsed

def myrec_to_bids(myrec_path, bids_dataset_object, session_id, task_id, participant_id_map, person_sessions=1000):
    """Convert .myrec file into BIDS format."""
    absolute_path_to_myrec = check_file(myrec_path)
    
    with tempfile.TemporaryDirectory() as unzip_dest:
        logging.debug(f"Working at {unzip_dest}")
        unzip_myrec(absolute_path_to_myrec, unzip_dest)
        
        with open(os.path.join(unzip_dest, "master_dir", "master.txt"), "r") as f:
            master_json = json.load(f)
        player_names = get_player_names(master_json)
        
        with open(os.path.join(unzip_dest, "count.txt"), "r") as f:
            stream_count = int(f.read().split('|')[1].split(';')[0])
        
        # Set DDRR semantics
        old_ddpp_semantics = get_dddp_semantics()
        set_dddp_semantics(angles=semantics_angles_unity(), axes=semantics_axes_unity())
        
        batches = [list(range(i, min(i + person_sessions, stream_count))) for i in range(0, stream_count, person_sessions)]
        
        for batch_index, batch in enumerate(batches):
            logging.debug(f"Processing batch {batch_index + 1}/{len(batches)}")
            
            data_records = []
            for stream_no in batch:
                stream_file = os.path.join(unzip_dest, f"stream{stream_no}_dir", "stream.txt")
                if os.path.exists(stream_file):
                    with open(stream_file, "r") as f:
                        data = f.readlines()
                    
                    for line in data:
                        parts = line.strip().split(";")
                        if len(parts) > 1:
                            header, entry = parts[0], parts[1:]
                            
                            for i, name in enumerate(player_names):
                                data_records.append({
                                    "stream_no": stream_no,
                                    "playername": name,
                                    "header": header,
                                    "entry": entry[i] if i < len(entry) else None
                                })
            
            df = pd.DataFrame(data_records)
            df["participant_id"] = df["playername"].map(participant_id_map)
            df["session_id"] = session_id
            df["task_id"] = task_id
            
            bids_write_motion_files(df, bids_dataset_object, append=True)
        
        # Restore old DDRR semantics
        set_dddp_semantics(**old_ddpp_semantics)
    
    logging.info("BIDS conversion completed.")
