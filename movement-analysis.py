import warnings

# including created packages -- these are to take the raw .myrec file, created a usable format, anonymize and cut down on subfolders, and rename variables
import raw_file_processor
import anonymizer # gitignored due to personal identifiable information
import variable_name_converter # gitignored, as it converts these variables to our specific naming convention for analysis, which isn't important

# created packages for variable calculations
import stu_ins_calculator
import stu_stu_calculator
import delta_calculator

from paths import raw_folder_path, processed_folder_path # gitignored, these are just your absolute paths
# e.g., "~/Desktop/name/folder1/folder2"

# next steps todo://
# 1. refactor variable calculators to look at notable columns in new names (after variable name converter)
# 2. implement raw_file_processor
# 3. refactor anonymizer
# 4. general refactor of dfs in subfiles

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