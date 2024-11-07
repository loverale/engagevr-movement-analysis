# this script will calculate delta between frames
def calculate_deltas_in_intervals(df, cols):
    # initialization to ensure empty df per file
    deltas = []
    num_rows = len(df)

    # does the thing
    for i in range(0, num_rows -1):
        delta = df.loc[i+1, cols].values - df.loc[i, cols].values
        deltas.append(np.abs(delta))  # Store the absolute delta

    return np.array(deltas)  # np has dope functions

# this function does all the delta calculations and file store.
def delta_process_file(file_path):
    # creates a file that stores deltas

    # extract participant ID from the file name
    participant_id = os.path.basename(file_path).split('.')[
        0]  # remember to rename files later

    # load the data
    data = pd.read_csv(file_path, delim_whitespace=True)

    # define columns for head and hand positions
    head_position = ['HeadPosition_x', 'HeadPosition_y', 'HeadPosition_z']
    head_rotation = ['HeadRotation_x', 'HeadRotation_y', 'HeadRotation_z']
    right_hand_position = ['RightHandPosition_x', 'RightHandPosition_y', 'RightHandPosition_z']
    left_hand_position = ['LeftHandPosition_x', 'LeftHandPosition_y', 'LeftHandPosition_z']
    right_hand_rotation = ['RightHandRotation_x', 'RightHandRotation_y', 'RightHandRotation_z']
    left_hand_rotation = ['LeftHandRotation_x', 'LeftHandRotation_y', 'LeftHandRotation_z']


    # calculate the deltas in 30-frame intervals for the entire dataset
    head_position_deltas = calculate_deltas_in_intervals(data, head_position)
    head_rotation_deltas = calculate_deltas_in_intervals(data, head_rotation)
    right_hand_position_deltas = calculate_deltas_in_intervals(data, right_hand_position)
    left_hand_position_deltas = calculate_deltas_in_intervals(data, left_hand_position)
    right_hand_rotation_deltas = calculate_deltas_in_intervals(data, right_hand_rotation)
    left_hand_rotation_deltas = calculate_deltas_in_intervals(data, left_hand_rotation)

    # calculate the average of the interval deltas
    avg_head_position_delta = np.sum(head_position_deltas) ## my thought process behind sum rather than mean -- better differentiates bt active and non-active (non-vr) users
    avg_head_rotation_delta = np.sum(head_rotation_deltas)

    #avg_head_delta = np.mean(np.sum(head_deltas)) # this is what using mean looks like
    avg_left_hand_position_delta = np.sum(left_hand_position_deltas)
    avg_right_hand_position_delta = np.sum(right_hand_position_deltas)
    avg_left_hand_rotation_delta = np.sum(left_hand_rotation_deltas)
    avg_right_hand_rotation_delta = np.sum(right_hand_rotation_deltas)

    # prepare the output
    result_df = pd.DataFrame({
        'participant_id': [participant_id],
        'avg_head_position': [avg_head_position_delta],
        'avg_head_rotation': [avg_head_rotation_delta],
        'avg_left_hand_position': [avg_left_hand_position_delta],
        'avg_right_hand_position': [avg_right_hand_position_delta],
        'avg_left_hand_rotation': [avg_left_hand_rotation_delta],
        'avg_right_hand_rotation': [avg_right_hand_rotation_delta]
    })

    return result_df

# not really needed for final computations. was just for descriptive
def row_counter(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        row_count = sum(1 for row in reader)  # Count the number of rows
    return row_count

# this function goes through each folder in the directory and runs the functions
def delta_all_files_in_folder(folder_path):
    # iterates through all the files and starts the path through other functions

    all_results = pd.DataFrame()  # master file
    row_count = 0

    # does the thing
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # .tsv check
        if file_name.endswith('.tsv'):
            print(f"    processing file {file_path}")
            row_count += row_counter(file_path)
            result_df = delta_process_file(file_path) # actual delta function
            all_results = pd.concat([all_results, result_df], ignore_index=True) # adds to master file

    # master file master file
    output_file = os.path.join(folder_path, 'all_participants_delta.csv')
    all_results.to_csv(output_file, index=False)
    print(f"All processed data saved to {output_file}")
    print(f"Row count: {row_count}")
