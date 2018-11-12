import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
import os
import gensim
from gensim.models import CoherenceModel


def compute_all_scores(modelname, corpus, id2word, texts, measure, limit, start=5, step=5):
    model_list, coherence_values = [], []

    def compute_model(modelname, corpus, id2word, topics):
        os.environ.update({'MALLET_HOME': r'b:/Courses/Mallet/'})
        mallet_path = 'b:\\Courses\\Mallet\\bin\\mallet'

        if modelname == 'LsiModel' or modelname == 'lsimodel':
            model = gensim.models.lsimodel.LsiModel(corpus=corpus,
                                                    num_topics=topics,
                                                    id2word=id2word,
                                                    chunksize=100)
        elif modelname == 'HdpModel' or modelname == 'hdpmodel':
            print(
                'Cannot compute varying models for HDP as it does not support number of topics.')
            return None
        elif modelname == 'LdaModel' or modelname == 'ldamodel':
            model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=id2word,
                                                    num_topics=topics,
                                                    random_state=100,
                                                    update_every=1,
                                                    chunksize=100,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True)
        elif modelname == 'LdaMallet' or modelname == 'ldamallet':
            model = gensim.models.wrappers.LdaMallet(mallet_path,
                                                     corpus=corpus,
                                                     num_topics=topics,
                                                     id2word=id2word)
        else:
            print('Invalid model!')
            return None

        return model

    for num_topics in range(start, limit + 1, step):
        computed_model = compute_model(modelname, corpus, id2word, num_topics)
        model_list.append(computed_model)

        coherencemodel = CoherenceModel(model=computed_model,
                                        texts=texts,
                                        dictionary=id2word,
                                        coherence=measure)
        coherence_values.append(coherencemodel.get_coherence())

    x = range(start, limit + 1, step)

    for n, score in zip(x, coherence_values):
        print(modelname, "Num Topics =", n,
              " has Coherence Value of", round(score, 4))

    return model_list, coherence_values
