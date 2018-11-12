from pprint import pprint
import numpy as np


def print_optimal_topics(model_list, all_scores):
    optimal_idx = np.argmax(all_scores)
    optimal_model = model_list[optimal_idx]
    optimal_model_topics = optimal_model.show_topics(formatted=False)
    pprint(optimal_model.print_topics())
    # Can add num_words = 10 to above print_topics() function
