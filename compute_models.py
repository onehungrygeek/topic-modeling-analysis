import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=DeprecationWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=DeprecationWarning)
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
import gensim
import os

# Update Mallet path and environment variable
# Mallet path for Windows 10
# os.environ.update({'MALLET_HOME': r'b:/Courses/Mallet/'})
# mallet_path = 'b:\\Courses\\Mallet\\bin\\mallet'

# Mallet path for Ubuntu 18.04
os.environ.update({'MALLET_HOME': r'/home/akshay/mallet/'})
mallet_path = '/home/akshay/mallet/bin/mallet'


def compute_model(model, corpus, id2word, num_topics=5):
    if model == 'LsiModel' or model == 'lsimodel':
        print('\nLSI Model Started\n')
        model = gensim.models.lsimodel.LsiModel(corpus=corpus,
                                                num_topics=num_topics,
                                                id2word=id2word,
                                                chunksize=100)
        topics = model.show_topics(formatted=False)
    elif model == 'HdpModel' or model == 'hdpmodel':
        print('\nHDP Model Started\n')
        model = gensim.models.hdpmodel.HdpModel(corpus=corpus,
                                                id2word=id2word,
                                                random_state=100,
                                                chunksize=100)
        topics = model.show_topics(formatted=False)
    elif model == 'LdaModel' or model == 'ldamodel':
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
    elif model == 'LdaMallet' or model == 'ldamallet':
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
