import os
import time
import json
import pandas as pd
from faker import Faker

# Fake name generator object
generateFake = Faker()
# Use any constant seed number to
# generate same fake names everytime
generateFake.seed(9999)

# os.getcwd() gives path for where this script is located. Append it
# with path to directory where all input JSON files are stored
# For eg. directory = /home/user/topic-model + /Inputs/JSONInputs/
input_files_directory = os.getcwd() + '/Inputs/JSON/Health/Health-JSON/'
output_files_directory = os.getcwd() + '/Output_Files/'
# List to store paths to all JSON files
filepaths_list = []

# List with all JSONs combined
combined_json = []

# Iterate over all filenames and append paths to
# files to filepaths_list is file ends with .json
for filename in os.listdir(input_files_directory):
    if filename.endswith(".json"):
        path_to_file = input_files_directory + filename
        filepaths_list.append(path_to_file)
        continue
    else:
        continue

# Iterate over all files in filepaths_list and append it to a big
# list so that we have all JSON files combined as one big JSON file
for file in sorted(filepaths_list):
    with open(file) as f:
        combined_json += json.loads(f.read())

# Convert the combined_json to a pandas dataframe
json_dataframe = pd.DataFrame.from_records(combined_json)

# Create a new column in the json_dataframe
# for fake usernames based on unique user IDs
json_dataframe['fake_username'] = json_dataframe.user.astype('category').cat.rename_categories(
    [generateFake.name() for x in range(1, json_dataframe.user.nunique() + 1)])

# Create a dictionary with all usernames and their respective contents/sentences
user_sentence_dict = json_dataframe.groupby(
    'fake_username')['content'].apply(lambda x: x.tolist())

# Reset json_dataframe index
json_dataframe = json_dataframe.reset_index()

# Set name of the index column to Line_Number
json_dataframe.rename(columns={'index': 'Line_Number'}, inplace=True)

# Set Line_Number column as the index
json_dataframe.set_index('Line_Number', inplace=True)

# Delelte newly created useless 'level_0' column from the json_dataframe
json_dataframe = json_dataframe.drop('level_0', 1)

# Rearrange columns in proper order for user to understand
# json_dataframe = json_dataframe[[
#     'user', 'fake_username', 'timeCode', 'content', 'reply', 'contentSimp']]

# Get current time
time_string = time.strftime("%m-%d-%Y_%H-%M-%S")

# Save dataframe as csv file with current timestamp
file_name = output_files_directory + 'json_dataframe' + '_' + time_string + '.csv'
print('\nSaved CSV file to:', file_name)
json_dataframe.to_csv(file_name, sep='\t', encoding='utf-8')
