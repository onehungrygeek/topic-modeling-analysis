import numpy as np
from pprint import pprint


def print_optimal_topics(model_list, all_scores):
    """
    This module selects a model from the list with maximum
    coherence score and prints the topics for that model.

    Arguments:
        model_list {list} -- List of computed models
        all_scores {list} -- List of coherence scores for respective computed models
    """

    # Index of the maximum coherence score
    optimal_idx = np.argmax(all_scores)
    # Optimal model for above index
    optimal_model = model_list[optimal_idx]
    # You can change number of words per topic by passing
    # num_words argument to print_topics() function below.
    # For example, pprint(optimal_model.print_topics(num_words=20))
    pprint(optimal_model.print_topics())
