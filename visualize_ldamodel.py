import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning, module='pyLDAvis')
warnings.filterwarnings(action='ignore', category=FutureWarning)
import os
import time
import pyLDAvis
import pyLDAvis.gensim


def visualize(model, corpus, id2word, time_string):
    current_dir = os.getcwd()
    # time_string = time.strftime("%m-%d-%Y_%H-%M-%S")
    vis = pyLDAvis.gensim.prepare(model, corpus, id2word)
    file = current_dir + '/Output_Files/LDA_vis_' + time_string + '.html'
    pyLDAvis.save_html(vis, file)
    print('\nSaving LDA model visualization to: ', file)
