## EngageVR Movement Analysis

This set of scripts are used to take a recording within EngageVR, and analyze across a number of different measures.

### General Pipeline
1. ```raw_file_processor.py``` takes the .myrec file from EngageVR, and creates a tidy format for each person within the recording.
2. ```anonymizer.py``` isn't included in this doc, but takes the names from the files and assigns a participant number. A template will be included soon, but for the time being isn't included for security
3. ```variable_name_converter.py``` isn't included either as it is needless, but simply renames the variable names from the EngageVR script and into shorthand (e.g., Avg_Left_Hand_Postion -> ALHP)
4. ```movement_analysis.py``` is the primary file. This calls upon a number of different scripts for different calculations (see below). *__This is what you need to run to get the variables of interest.__*

### Variable Calculations
#### Delta Calculations (delta_calculator.py)
- General movement (deltas)
- LR Hand Distance Delta (inferring whether individual is in a headset or on PC/mobile)
- Row count (for descriptives)

#### Stu_Ins Gaze/Distance (stu_ins_calculator.py)
- Student-instructor oneway direct gaze
- Student-instructor oneway peripheral gaze
- Student-instructor mutual direct gaze
- Student-instructor mutual peripheral gaze
- Student-instructor average distance

#### Stu_Stu Gaze/Distance (stu_ins_calculator.py)
- Student-student oneway direct gaze
- Student-student oneway peripheral gaze
- Student-student mutual direct gaze
- Student-student mutual peripheral gaze
- Student-student average distance
