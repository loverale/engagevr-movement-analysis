from paths import gaze_output_path

# global vars
gaze_towards_other = 0
no_match = []
stop_running = False


def stustu_gaze_process_file(file_path, comp_stu):
    global gaze_towards_other, no_match, folder_path, stop_running

    comp_file_path = os.path.join(folder_path, comp_stu)
    comp_data = pd.read_csv(comp_file_path, delim_whitespace=True)
    stu_data = pd.read_csv(file_path, delim_whitespace=True)
    comp_data.set_index('full_frame_no', inplace=True) # sets index for faster checking

    # determines rows to look for
    rows_to_iterate = ['full_frame_no', 'HeadPosition_x', 'HeadPosition_y', 'HeadPosition_z', 'HeadRotation_x', 'HeadRotation_y', 'HeadRotation_z']
    if not no_match:
        for i, row in stu_data[rows_to_iterate].iterrows():
            row_number = row['full_frame_no']
            stu_pos = row['HeadPosition_x'], row['HeadPosition_y'], row['HeadPosition_z']
            stu_rot = row['HeadRotation_x'], row['HeadRotation_y'] # gaze only needs x, y, since roll (direction of z) can be inferred by sin(pitch)

            if row_number in comp_data.index:
                corresponding_row = comp_data.loc[row_number]
                comp_pos = corresponding_row['HeadPosition_x'], corresponding_row['HeadPosition_y'], corresponding_row[
                    'HeadPosition_z']
                gaze_towards_other += calculate_gaze_towards_other(stu_pos, stu_rot, comp_pos)
            else:
                no_match.append(row_number)
                continue
    else:
        temp = len(no_match)
        for index in range(temp):
            locator = stu_data.loc[no_match[index]]
            row_number = locator['full_frame_no']
            if row_number in comp_data.index:
                stu_row = stu_data.loc[locator]
                stu_pos = [
                    stu_row["HeadPosition_x"],
                    stu_row["HeadPosition_y"],
                    stu_row["HeadPosition_z"]
                ]
                stu_rot = [
                    stu_row["HeadRotation_x"],
                    stu_row["HeadRotation_y"] # still only needs x y
                ]
                corresponding_row = comp_data.loc[locator]
                comp_pos = [corresponding_row['HeadPosition_x'], corresponding_row['HeadPosition_y'], corresponding_row[
                    'HeadPosition_z']]
                gaze_towards_other += calculate_gaze_towards_other(stu_pos, stu_rot, comp_pos)
                no_match.pop(index) # removes so no endless process, also, ignore bandaid fix of turning into int

                if not no_match:
                    stop_running = True # stops running no_match
                    break
            else:
                continue

# separate from stuins, as iteration will need another approach for optimization
def stustu_gaze_process_all_files(folder_path):
    # iterates through all the files and starts the path through other functions

    all_results = pd.DataFrame()  # master file
    row_count = 0
    all_files_disorganized = []

    # does the thing
    for file_name in os.listdir(folder_path):
        if not ("pPROF" in file_name) and not ("pTA" in file_name):
            all_files_disorganized.append(file_name)

    row_count = 0
    global gaze_towards_other, stop_running, no_match

    for file_name in all_files_disorganized:
        if file_name.endswith('.tsv'):  # .tsv check
            print(f"    processing {file_name}")
            file_path = os.path.join(folder_path, file_name)
            class_no = os.path.basename(file_path).split('c')[1]
            participant_id = os.path.basename(file_path).split('.')[0]
            comparison_list = [file for file in all_files_disorganized if class_no in file and participant_id not in file]

            for comparison in comparison_list:
                if stop_running:
                    break # gets us out of the nightmare
                stustu_gaze_process_file(file_path, comparison)

        no_match = []
        # prepare the output
        gaze_towards_student = gaze_towards_other / 30
        gaze_towards_student = round(gaze_towards_student, 2)
        result_df = pd.DataFrame({
            'participant_id': [participant_id],
            'stustugaze': [gaze_towards_student]
        })

        gaze_towards_other = 0  # re-initialize
        stop_running = False

        all_results = pd.concat([all_results, result_df], ignore_index=True)

    # master file
    output_path = os.path.join(gaze_output_path, 'all_participants_delta.csv')
    all_results.to_csv(output_file, index=False)
    print(f"    All processed data saved to {output_file}")
    print(f"    Row count: {row_count}")
