from paths import gaze_output_path
import pandas as pd
import numpy as np
import os
import csv

# global vars
direct_gaze_towards_instructor = 0
peripheral_gaze_towards_instructor = 0
opposite_gaze_towards_instructor = 0

# fairly easy but probably not optimal
def calculate_distance(student_pos_x, student_pos_y, student_pos_z, prof_pos_x, prof_pos_y, prof_pos_z):

    # components of distance function
    x2 = pow(student_pos_x - prof_pos_x, 2)
    y2 = pow(student_pos_y - prof_pos_y, 2)
    z2 = pow(student_pos_z - prof_pos_z, 2)

    # calculates the distance
    distance = np.sqrt(x2 + y2 + z2)

    return distance

# This function should return a general idea of what direction the student is looking.
# refer to trigonometry textbooks
def vector_from_rotation(rotation):
    # Assume rotation is a tuple (pitch, yaw) in degrees
    pitch, yaw = np.radians(rotation)

    # Calculate the forward vector from the head rotation (simplified version)
    forward_x = np.cos(pitch) * np.cos(yaw)
    forward_y = np.cos(pitch) * np.sin(yaw)
    forward_z = np.sin(pitch)

    return np.array([forward_x, forward_y, forward_z])

# general idea of this function is to figure out where the student is looking, and see if the other persons coordinates are within
# that field of view.
# function returns 1 for each line calculation, goal is to divide by 30 to get seconds looked at instructor
def calculate_gaze_towards_other(student_pos, student_rotation, other_pos, threshold=0.75):
    # Get the gaze direction of student
    student_gaze_direction = vector_from_rotation(student_rotation)

    # Calculate the direction from student to instructor
    direction_to_other = np.array(other_pos) - np.array(student_pos)
    direction_to_other = direction_to_other / np.linalg.norm(direction_to_other)  # Normalize

    # Calculate the dot product between the gaze direction and the direction to B
    dot_product = np.dot(student_gaze_direction, direction_to_other)

    global direct_gaze_towards_instructor, peripheral_gaze_towards_instructor, opposite_gaze_towards_instructor

    # Check if the dot product is above the threshold to assume direct gaze
    # threshhold is fairly arbitrary here, but general idea is there. probably will reduce to 70-80 if i can find some FoV lit
    if(dot_product > threshold):
        direct_gaze_towards_instructor += 1
    # assume 0-.749 is peripheral gaze
    elif dot_product > 0 and dot_product < threshold:
        peripheral_gaze_towards_instructor += 1

# this function takes the given student file, finds the appropriate instructor profile (pPROF), and sends to gaze function
def stuins_gaze_distance_process_file(file_path, pPROF):
    # bringing global variable, c# habits die hard
    global direct_gaze_towards_instructor, peripheral_gaze_towards_instructor, opposite_gaze_towards_instructor

    # temp variables parsing file name
    participant_id = os.path.basename(file_path).split('.')[
        0]  # remember to rename files later
    class_no = os.path.basename(file_path).split('c')[
        1]  # remember to rename files later

    #print(class_no)

    correct_prof = [file for file in pPROF if class_no in file]
    global folder_path
    correct_prof = os.path.join(folder_path, correct_prof[0])

    prof_data = pd.read_csv(correct_prof, delim_whitespace=True)

    stu_data = pd.read_csv(file_path, delim_whitespace=True)
    #prof_data = pd.read_csv(correct_prof, delim_whitespace=True) # now checked by prveious if function
    prof_data.set_index('full_frame_no', inplace=True) # sets index for faster checking

    distance_df = [] # re-initialize

    # determines rows to look for
    rows_to_iterate = ['full_frame_no', 'HeadPosition_x', 'HeadPosition_y', 'HeadPosition_z', 'HeadRotation_x', 'HeadRotation_y', 'HeadRotation_z']
    for i, row in stu_data[rows_to_iterate].iterrows():
        row_number = row['full_frame_no']
        stu_pos = row['HeadPosition_x'], row['HeadPosition_y'], row['HeadPosition_z']
        stu_rot = row['HeadRotation_x'], row['HeadRotation_y'] # gaze only needs x, y, since roll (direction of z) can be inferred by sin(pitch)

        if row_number in prof_data.index:
            corresponding_row = prof_data.loc[row_number]
            ins_pos = corresponding_row['HeadPosition_x'], corresponding_row['HeadPosition_y'], corresponding_row[
                'HeadPosition_z']
            direct_gaze_towards_instructor += calculate_gaze_towards_other(stu_pos, stu_rot, ins_pos) # moved to elsewhe
            distance_df.append(calculate_distance(row['HeadPosition_x'], row['HeadPosition_y'], row['HeadPosition_z'], corresponding_row['HeadPosition_x'], corresponding_row['HeadPosition_y'], corresponding_row[
                'HeadPosition_z']))
        else:
            continue

    #length = len(file_path)
    student_total_time = (stu_data['full_frame_no'].iloc[-1] - stu_data['full_frame_no'].iloc[0]) / 30
    student_total_time = round(student_total_time, 2) # rounding to 2 for easy viewing
    direct_gaze_towards_instructor = direct_gaze_towards_instructor / 30
    direct_gaze_towards_instructor = round(direct_gaze_towards_instructor, 2)
    peripheral_gaze_towards_instructor = peripheral_gaze_towards_instructor / 30
    peripheral_gaze_towards_instructor = round(peripheral_gaze_towards_instructor, 2)
    opposite_gaze_towards_instructor = opposite_gaze_towards_instructor / 30
    opposite_gaze_towards_instructor = round(opposite_gaze_towards_instructor, 2)

    # prepare the output
    result_df = pd.DataFrame({
        'participant_id': [participant_id],
        'dirgazeins': [direct_gaze_towards_instructor],
        'pergazeins': [peripheral_gaze_towards_instructor],
        'oppgazeins': [opposite_gaze_towards_instructor],
        'total_time': [student_total_time],
        'stuinsdis': [np.mean(distance_df)]
    })

    return result_df

# process_all_files_in_folder, but for gaze not delta
def stuins_gaze_process_all_files(folder_path):
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
    global direct_gaze_towards_instructor, peripheral_gaze_towards_instructor, opposite_gaze_towards_instructor

    for file_name in all_files:
        for sub_file in file_name:
            if sub_file.endswith('.tsv'): # .tsv check
                print(f"    processing {sub_file}")

                file_path = os.path.join(folder_path, sub_file)
                result_df = stuins_gaze_distance_process_file(file_path, pPROF)
                direct_gaze_towards_instructor = 0 # re-initialize
                peripheral_gaze_towards_instructor = 0 # re-initialie
                opposite_gaze_towards_instructor = 0
                all_results = pd.concat([all_results, result_df], ignore_index=True)

    # master file
    output_file = os.path.join(gaze_output_path, 'all_participants_gaze.csv')
    all_results.to_csv(output_file, index=False)
    print(f"    All processed data saved to {output_file}")
    print(f"    Row count: {row_count}")
