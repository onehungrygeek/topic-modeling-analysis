import os
import sys
import glob
import pickle
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt

style = style_from_dict(
    {
        Token.Separator: "#cc5454",
        Token.QuestionMark: "#f4511e bold",
        Token.Selected: "#f4511e bold",
        Token.Pointer: "#1976d2 bold",
        Token.Instruction: "#1976d2",
        Token.Answer: "#f4511e bold",
        Token.Question: "",
    }
)

current_directory = os.getcwd()

model, topics, dataset = None, None, None

model_files_directory = os.path.join(current_directory, "Saved_Models/")
model_pickles = glob.glob(model_files_directory + "*.pkl")
model_pickles.sort(key=lambda x: os.path.getmtime(x), reverse=True)

dataset_files_directory = os.path.join(current_directory, "Datasets/")
dataset_files = glob.glob(dataset_files_directory + "*.txt")
dataset_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

questions = [
    {
        # Default
        "type": "rawlist",
        "message": "Select one option:",
        "name": "default",
        "choices": [
            "Run topic modeling analysis on a dataset.",
            "Load already saved model and topics.",
            "Exit"
        ],
    },
    {
        # Number of words to output
        "type": "input",
        "name": "num_words",
        "message": "Enter number of words to output from this model:",
        "default": "10",
        "validate": lambda val: val.isdigit()
        or "Please enter a valid integer. (Default: 10) ",
    },
    {
        # Model
        "type": "rawlist",
        "message": "Select a model file (Only recent 8 displayed):",
        "name": "model",
        "choices": [os.path.basename(file) for file in model_pickles[:8]]
        + ["Enter name instead..."],
    },
    {
        # Dataset
        "type": "rawlist",
        "message": "Select a dataset (Only recent 8 displayed):",
        "name": "dataset",
        "choices": [os.path.basename(file) for file in dataset_files[:8]]
        + ["Enter name instead..."],
    },
]


def file_error_checker(file):
    if not os.path.isfile(file):
        raise SystemExit(
            "\nERROR: File not found. Please check again!\n\nScript exited..."
        )
    elif not (os.path.getsize(file) > 0):
        raise SystemExit(
            "\nERROR: File might be empty. Please check again!\n\nScript exited..."
        )


def model_pickle_loader():
    choice_number = 2
    directory = model_files_directory

    print()

    prompter = prompt(questions[choice_number], style=style)
    choice = prompter["model"]

    if choice == "Enter name instead...":
        choice = input("\nEnter file name with extension:\t")

    filepath = os.path.join(directory, choice)

    file_error_checker(filepath)

    with open(filepath, "rb") as file:
        unpickled_object = pickle.Unpickler(file)
        data = unpickled_object.load()

    return data


def dataset_chooser():
    prompter = prompt(questions[3], style=style)
    choice = prompter["dataset"]
    if choice == "Enter name instead...":
        choice = input("\nEnter file name with extension:\t")
    filepath = os.path.join(dataset_files_directory, choice)
    file_error_checker(filepath)
    return filepath


def inquire():
    print()
    prompter = prompt(questions[0], style=style)
    if prompter["default"] == questions[0]["choices"][0]:
        print()
        filepath = dataset_chooser()
        return filepath
    elif prompter["default"] == questions[0]["choices"][1]:
        model = model_pickle_loader()
        print()
        prompter = prompt(questions[1], style=style)
        num_words = int(prompter["num_words"])
        print("\nPrinting topics from selected model pickle...\n")
        pprint(model.show_topics(num_words=num_words))
        sys.exit()
    else:
        print("\nScript exited...")
        sys.exit()


if __name__ == "__main__":
    inquire()
