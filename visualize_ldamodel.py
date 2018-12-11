# Library imports
# warnings module to surpress all FutureWarnings
import warnings
warnings.filterwarnings(
    action='ignore', category=FutureWarning, module='pyLDAvis')
warnings.filterwarnings(action='ignore', category=FutureWarning)
import os
import time
import pyLDAvis
import pyLDAvis.gensim


def visualize(model, corpus, id2word, time_string):
    """
    This module uses pyLDAvis library for LDA visualization

    Arguments:
        model {LdaModel} -- LdaModel computed from gensim.model.ldamodel.LdaModel
        corpus {list} -- List of corpus created from preprocessed texts
        id2word {Dictionary} -- Dictionary of ids with mapped words
        time_string {str} -- Current timestamp
    """

    # Get current working directory and save visualization to Output_Files directory
    current_dir = os.getcwd()
    # Visualize
    vis = pyLDAvis.gensim.prepare(model, corpus, id2word)
    # Save visualization into file_name
    file_name = current_dir + '/Output_Files/LDA_vis_' + time_string + '.html'
    pyLDAvis.save_html(vis, file_name)
    print('\nSaving LDA model visualization to: ', file_name)
