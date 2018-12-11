# Library imports
# warnings module to surpress all UserWarnings, DeprecationWarnings and RuntimeWarnings
import warnings
warnings.filterwarnings(action='ignore',
                        category=UserWarning,
                        module='gensim')
warnings.filterwarnings(action='ignore',
                        category=DeprecationWarning,
                        module='gensim')
warnings.filterwarnings(action='ignore',
                        category=DeprecationWarning)
warnings.filterwarnings(action='ignore',
                        category=RuntimeWarning)
import os
import gensim

# Update Mallet path and environment variable so
# that LdaMallet model in gensim works properly
# --- Mallet path for Windows 10
# os.environ.update({'MALLET_HOME': r'b:/Courses/Mallet/'})
# mallet_path = 'b:\\Courses\\Mallet\\bin\\mallet'
# --- Mallet path for Ubuntu 18.04
os.environ.update({'MALLET_HOME': r'/home/akshay/mallet/'})
mallet_path = '/home/akshay/mallet/bin/mallet'


def compute_model(model_name, corpus, id2word, num_topics=5):
    """
    This module computes various topic models from the gensim library.

    Arguments:
        model_name {str} -- Name of the model
        corpus {list} -- List of corpus created from preprocessed texts
        id2word {Dictionary} -- Dictionary of ids with mapped words

    Keyword Arguments:
        num_topics {int} -- Number of topics as a parameter to gensim model computation (default: {5})

    Returns:
        gensim.models.MODEL, list -- Return the computed model and also respective model topics as a list
    """

    # LSI Model and Topics
    if model_name == 'LsiModel' or model_name == 'lsimodel' or model_name == 'lsi':
        print('\nLSI Model Started\n')
        model = gensim.models.lsimodel.LsiModel(corpus=corpus,
                                                num_topics=num_topics,
                                                id2word=id2word,
                                                chunksize=100)
        topics = model.show_topics(formatted=False)
    # HDP Model and Topics
    elif model_name == 'HdpModel' or model_name == 'hdpmodel' or model_name == 'hdp':
        print('\nHDP Model Started\n')
        model = gensim.models.hdpmodel.HdpModel(corpus=corpus,
                                                id2word=id2word,
                                                random_state=100,
                                                chunksize=100)
        topics = model.show_topics(formatted=False)
    # LDA Model and Topics
    elif model_name == 'LdaModel' or model_name == 'ldamodel' or model_name == 'lda':
        print('\nLDA Model Started\n')
        model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=num_topics,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)
        topics = model.show_topics(formatted=False)
    # LDAMallet Model and Topics
    elif model_name == 'LdaMallet' or model_name == 'ldamallet' or model_name == 'ldamallet':
        print('\nLDA Mallet Model Started\n')
        model = gensim.models.wrappers.LdaMallet(mallet_path,
                                                 corpus=corpus,
                                                 num_topics=num_topics,
                                                 id2word=id2word)
        topics = model.show_topics(formatted=False)
    else:
        print('Invalid model!')
        return None, None

    return model, topics
