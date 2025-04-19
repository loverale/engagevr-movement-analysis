import os
import re
import pandas as pd
from pathlib import Path

# all credit goes to @markromanmiller. This file is simply a Python version of the following public Github in R:
# https://github.com/social-spatial-interaction-lab/rbids/blob/main/R/rbids.R

def bids(root: str, readonly: bool = True):
    """Initialize a BIDS dataset object."""
    if not os.path.exists(root) and readonly:
        raise ValueError(f"Root directory `{root}` does not exist")
    
    root = os.path.abspath(root)
    return {
        "root": root,
        "all_files": [str(p) for p in Path(root).rglob("*")],
        "readonly": readonly
    }

def bids_all_files(bd, full_names=True):
    """Return all files in the BIDS dataset."""
    return pd.DataFrame({"file_path": bd["all_files"]})

def bids_match_path(bd, pattern, full_names=True):
    """Search for files matching a regex pattern."""
    matches = [f for f in bd["all_files"] if re.search(pattern, f)]
    return pd.DataFrame({"file_path": matches})

def bids_motion_regex():
    """Regex pattern for BIDS motion files."""
    return (r"^sub-(?P<participant_id>\w+)/ses-(?P<session_id>\w+)/motion/"
            r"sub-(?P=participant_id)_ses-(?P=session_id)_task-(?P<task_label>\w+)_motion.tsv$")

def bids_motion(bd, full_names=True):
    """Retrieve motion files from a BIDS dataset."""
    return bids_match_path(bd, bids_motion_regex(), full_names)

def bids_read_tsvs(bids_table):
    """Read and return TSV files as DataFrames."""
    return pd.concat([pd.read_csv(f, sep="\t") for f in bids_table["file_path"]])

def write_tsv_at(df, file_path, append=False):
    """Write DataFrame to a TSV file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, sep="\t", index=False, mode='a' if append else 'w', header=not append)

def bids_write_motion_file(participant_id, session_id, task_id, data, bids_dataset, append=False):
    """Write a motion file to BIDS dataset."""
    if bids_dataset["readonly"]:
        raise ValueError("BIDS dataset is readonly. Cannot write.")
    
    file_path = os.path.join(
        bids_dataset["root"], f"sub-{participant_id}", f"ses-{session_id}",
        "motion", f"sub-{participant_id}_ses-{session_id}_task-{task_id}_motion.tsv"
    )
    write_tsv_at(data, file_path, append)
    return "success"

def bids_write_motion_files(df, bids_dataset, append=False):
    """Write multiple motion files."""
    required_columns = {"participant_id", "session_id", "task_id", "data"}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing columns: {', '.join(missing)}")
    
    for _, row in df.iterrows():
        bids_write_motion_file(row.participant_id, row.session_id, row.task_id, row.data, bids_dataset, append)
