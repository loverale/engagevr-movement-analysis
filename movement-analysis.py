import pandas as pd
import numpy as np
import os
import csv
import warnings

# including created packages
import anonymizer # gitignored due to personal identifiable information
import raw_file_processor
import stu_ins_calculator
import stu_stu_calculator
import delta_calculator

# gitignored, these are just your absolute paths, 
from paths import raw_folder_path, processed_folder_path 
# e.g., "~/Desktop/name/folder1/folder2"

gaze_towards_instructor = 0
gaze_towards_other = 0
no_match = []
stop_running = False

# not really needed for final computations. was just for descriptive
def row_counter(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        row_count = sum(1 for row in reader)  # Count the number of rows
    return row_count

######

# never replicate this line of code
# do as i say not as i do
warnings.filterwarnings("ignore", category=FutureWarning)
# end of bad practices

#global folder_path
print("PROCESSING DELTA STARTED")
#delta_all_files_in_folder(processed_folder_path) # starts the delta calcs

print("PROCESSING STU-INS GAZE & DISTANCE")
# stuins_gaze_process_all_files(processed_folder_path) # starts both gaze and distance (at same time for optimization reasons)

print("PROCESSING STU-STU GAZE")
#stustu_gaze_process_all_files(processed_folder_path)