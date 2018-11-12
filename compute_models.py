import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
import gensim
import os


def compute_model(model, corpus, id2word):
    # Mallet Path Update
    os.environ.update({'MALLET_HOME': r'b:/Courses/Mallet/'})
    mallet_path = 'b:\\Courses\\Mallet\\bin\\mallet'

    if model == 'LsiModel' or model == 'lsimodel':
        print('\nLSI Model Started\n')
        model = gensim.models.lsimodel.LsiModel(corpus=corpus,
                                                num_topics=10,
                                                id2word=id2word,
                                                chunksize=100)
        topics = model.show_topics(formatted=False)
        # print('LSI Model Ended\n\n')
    elif model == 'HdpModel' or model == 'hdpmodel':
        print('\nHDP Model Started\n')
        model = gensim.models.hdpmodel.HdpModel(corpus=corpus,
                                                id2word=id2word,
                                                random_state=100,
                                                chunksize=100)
        topics = model.show_topics(formatted=False)
        # print('HDP Model Ended\n\n')
    elif model == 'LdaModel' or model == 'ldamodel':
        print('\nLDA Model Started\n')
        model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=10,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)
        topics = model.show_topics(formatted=False)
        # print('LDA Model Ended\n\n')
    elif model == 'LdaMallet' or model == 'ldamallet':
        print('\nLDA Mallet Model Started\n')
        model = gensim.models.wrappers.LdaMallet(mallet_path,
                                                 corpus=corpus,
                                                 num_topics=10,
                                                 id2word=id2word)
        topics = model.show_topics(formatted=False)
        # print('LDA Mallet Model Ended\n\n')
    else:
        print('Invalid model!')
        return None, None

    return model, topics
