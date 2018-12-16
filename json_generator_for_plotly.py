# Library imports
import os
import csv
import glob
import json


def json_generator():
    """
    This module takes in the json inputs and appends respective dominant topics, keywords and probabilities for each entry.
    The corresponding outputs are saved in a directory as .json files.
    """

    # Directory for input files
    input_files_directory = os.getcwd() + '/Inputs/JSON/Health/Health-JSON/'
    # List of paths for all the required .json files starting with name 'Print Page - Healthcare'
    input_file_paths = glob.glob(
        input_files_directory + 'Print Page - Healthcare*')
    # Sort file paths from A to Z
    input_file_paths.sort()

    # List to store names of all input files we are operating with
    input_file_names = []
    for current_file_name in input_file_paths:
        input_file_names.append(os.path.basename(current_file_name))

    # A list to store that reads initial JSON objects and we then add extra entries to it
    all_data = []

    # Load JSON data file by file
    for current_file in input_file_paths:
        with open(current_file, "r") as read_file:
            all_data.append(json.load(read_file))

    # Open category.csv file and read it to a list
    with open(input_files_directory + 'category.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        category_list = []
        for row in csv_reader:
            category_list.append(row)

    # List to store a list of lists for topics, keywords and probabilities
    total_topics, total_keywords, total_probablities = [], [], []
    # Reformat the original entries and append them respectively in above declared lists
    for i in range(len(all_data)):
        # Local lists for topics, keywords and probabilities in current file
        topics, keywords, probablities = [], [], []
        # Dictionary to store probabilities for all topics
        prob_dict = {}
        for j in range(1, len(all_data[i]) + 1):
            topics.append(category_list[j][7].capitalize())
            seperated_keywords = ", ".join(
                word for word in category_list[j][0].split())
            keywords.append(seperated_keywords)
            for k in range(1, 7):
                prob_dict[category_list[0]
                          [k].capitalize()] = category_list[j][k] + ' %'
            probablities.append(prob_dict)
        total_topics.append(topics)
        total_keywords.append(keywords)
        total_probablities.append(probablities)

    # Insert new entries into JSON objects one by one
    for i in range(len(all_data)):
        for j in range(len(all_data[i])):
            all_data[i][j].pop('contentSimp', None)
            all_data[i][j]['dominant_topic'] = total_topics[i][j]
            all_data[i][j]['keywords'] = total_keywords[i][j]
            all_data[i][j]['topic_probablities'] = total_probablities[i][j]

    # Set the output directory for saving .json files
    # Note: Create 'JSON' directory if it does not exist
    output_files_directory = os.getcwd() + '/Output_Files/JSON/'
    generic_output_file_name = output_files_directory + 'Output_'
    output_file_names = [generic_output_file_name +
                         current_file for current_file in input_file_names]

    # Open/Create output .json files one by one with same
    # input file names and dump respective JSON data to them
    for i in range(len(output_file_names)):
        current_file = output_file_names[i]
        with open(current_file, 'w') as file:
            json.dump(all_data[i], file)

    print("\nAll output .json files saved to:", output_files_directory)


if __name__ == '__main__':
    json_generator()
