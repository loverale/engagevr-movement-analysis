import pandas as pd

# all credit for this goes to @markromanmiller, this file is simply a Python version of the following public Github in R:
# https://github.com/markromanmiller/dddr

def semantics_angles_unity():
    """Define semantics for angles in Unity."""
    return {
        "unit": "degrees",
        "convention": "Unity"
    }

def semantics_axes_unity():
    """Define semantics for axes in Unity."""
    return {
        "forward": "Z+",
        "up": "Y+",
        "right": "X+"
    }

def set_dddp_semantics(angles, axes):
    """Set DDPP semantics globally."""
    global DDPP_SEMANTICS
    DDPP_SEMANTICS = {
        "angles": angles,
        "axes": axes
    }

def get_dddp_semantics():
    """Retrieve current DDPP semantics."""
    return DDPP_SEMANTICS

def parse_stream_data(stream_text, player_names):
    """Parse a stream text file into structured data."""
    records = []
    lines = stream_text.strip().split("\n")
    for line in lines:
        parts = line.split(";")
        if len(parts) > 1:
            header, entries = parts[0], parts[1:]
            for i, name in enumerate(player_names):
                records.append({
                    "playername": name,
                    "header": header,
                    "entry": entries[i] if i < len(entries) else None
                })
    return pd.DataFrame(records)

def transform_data(df):
    """Transform and pivot data for BIDS compatibility."""
    df = df.pivot_table(index=["playername"], columns="header", values="entry", aggfunc="first").reset_index()
    return df
