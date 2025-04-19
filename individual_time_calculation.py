from paths import gaze_output_path
import pandas as pd
import numpy as np
import os
import csv

# this function takes the given student file, finds the appropriate instructor profile (pPROF), and sends to gaze function
def ind_time_process_file(file_path):
    # bringing global variable, c# habits die hard
    global direct_gaze_towards_instructor, peripheral_gaze_towards_instructor, opposite_gaze_towards_instructor

    # temp variables parsing file name
    participant_id = os.path.basename(file_path).split('.')[
        0]  # remember to rename files later
    class_no = os.path.basename(file_path).split('c')[
        1]  # remember to rename files later

    stu_data = pd.read_csv(file_path, delim_whitespace=True)

    start_time = stu_data['frameno'][0] / 30
    end_time = stu_data['frameno'][-1] / 30
    total_time = end_time - start_time

    # prepare the output
    result_df = pd.DataFrame({
        'participant_id': [participant_id],
        'start_time': [start_time],
        'end_time': [end_time],
        'class_no': [class_no],
        'total_time': [total_time]
    })

    return result_df

# process_all_files_in_folder, but for gaze not delta
def ind_time_process_all(folder_path):
    # iterates through all the files and starts the path through other functions

    all_results = pd.DataFrame()  # master file master file
    row_count = 0

    # also bad coding practice, but the more efficient p1 = p3 = ... is breaking the script
    # this is our numbering for the participants to include in the analysis
    #region
    p1 = []
    p3 = []
    p4 = []
    p5 = []
    p6 = []
    p7 = []
    p8 = []
    p9 = []
    p10 = []
    p11 = []
    p12 = []
    p14 = []
    p15 = []
    p16 = []
    p17 = []
    p18 = []
    p19 = []
    p20 = []
    p21 = []
    p22 = []
    p24 = []
    p25 = []
    p26 = []
    p27 = []
    p28 = []
    p29 = []
    p30 = []
    p31 = []
    p34 = []
    p35 = []
    pPROF = []
    #endregion

    # does the thing
    for file_name in os.listdir(folder_path):

        #more bad coding practice (see above)
        # this creates a series of sublists of each participant, basically takes the folder of everything and subdivides
        #region
        # _ added to p1 and p3 to avoid adding files from p10, p30, etc
        if("p1_" in file_name):
            p1.append(file_name)
        if("p3_" in file_name):
            p3.append(file_name)
        if ("p4" in file_name):
            p4.append(file_name)
        if("p5" in file_name):
            p5.append(file_name)
        if("p6" in file_name):
            p6.append(file_name)
        if("p7" in file_name):
            p7.append(file_name)
        if("p8" in file_name):
            p8.append(file_name)
        if("p9" in file_name):
            p9.append(file_name)
        if("p10" in file_name):
            p10.append(file_name)
        if("p11" in file_name):
            p11.append(file_name)
        if("p12" in file_name):
            p12.append(file_name)
        if("p14" in file_name):
            p14.append(file_name)
        if("p15" in file_name):
            p15.append(file_name)
        if("p16" in file_name):
            p16.append(file_name)
        if ("p17" in file_name):
            p17.append(file_name)
        if("p18" in file_name):
            p18.append(file_name)
        if("p19" in file_name):
            p19.append(file_name)
        if("p20" in file_name):
            p20.append(file_name)
        if("p21" in file_name):
            p21.append(file_name)
        if("p22" in file_name):
            p22.append(file_name)
        if("p24" in file_name):
            p24.append(file_name)
        if("p25" in file_name):
            p25.append(file_name)
        if("p26" in file_name):
            p26.append(file_name)
        if("p27" in file_name):
            p27.append(file_name)
        if("p28" in file_name):
            p28.append(file_name)
        if("p29" in file_name):
            p29.append(file_name)
        if("p30" in file_name):
            p30.append(file_name)
        if("p31" in file_name):
            p31.append(file_name)
        if("p34" in file_name):
            p34.append(file_name)
        if("p35" in file_name):
            p35.append(file_name)
        if("pPROF" in file_name):
            pPROF.append(file_name)
        #endregion
    all_files = [p1, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p14, p15, p16, p17, p18, p19, p20, p21, p22, p24, p25, p26, p27, p28, p29, p30, p31, p34, p35]

    row_count = 0

    for file_name in all_files:
        for sub_file in file_name:
            if sub_file.endswith('.tsv'): # .tsv check
                print(f"    processing {sub_file}")

                file_path = os.path.join(folder_path, sub_file)
                result_df = ind_time_process_file(file_path)
                all_results = pd.concat([all_results, result_df], ignore_index=True)

    # master file
    output_file = os.path.join(gaze_output_path, 'all_participants_time.csv')
    all_results.to_csv(output_file, index=False)
    print(f"    All processed data saved to {output_file}")
    print(f"    Row count: {row_count}")