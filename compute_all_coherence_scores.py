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
from gensim.models import CoherenceModel

# Update Mallet path and environment variable so
# that LdaMallet model in gensim works properly
# --- Mallet path for Windows 10
# os.environ.update({'MALLET_HOME': r'b:/Courses/Mallet/'})
# mallet_path = 'b:\\Courses\\Mallet\\bin\\mallet'
# --- Mallet path for Ubuntu 18.04
os.environ.update({'MALLET_HOME': r'/home/akshay/mallet/'})
mallet_path = '/home/akshay/mallet/bin/mallet'


def compute_all_scores(model_name, corpus, id2word, texts, measure, max_topics, start=5, step=5):
    """
    This module computes coherence scores for increasing number of topics.

    Arguments:
        model_name {str} -- Name of the model
        corpus {list} -- List of corpus created from preprocessed texts
        id2word {Dictionary} -- Dictionary of ids with mapped words
        texts {list} -- List of preprocessed input words
        measure {str} -- Name of the coherence score you want to use. Possible measures: c_v, c_uci, c_npmi, u_mass
        max_topics {int} -- Maximum number of topics used in computing various coherence scores

    Keyword Arguments:
        start {int} -- Start value for x-axis values (default: {5})
        step {int} -- Steps for values on x-axis (default: {5})

    Returns:
        list, list -- List of computed models, List of coherence scores for respective computed models
    """

    def compute_model(model_name, corpus, id2word, num_topics):
        """
        This module computes various topic models from the gensim library.

        Arguments:
            model_name {str} -- Name of the model
            corpus {list} -- List of corpus created from preprocessed texts
            id2word {Dictionary} -- Dictionary of ids with mapped words

        Keyword Arguments:
            num_topics {int} -- Number of topics as a parameter to gensim model computation (default: {5})

        Returns:
            gensim.models.MODEL -- Return the computed model
        """

        # LSI Model
        if model_name == 'LsiModel' or model_name == 'lsimodel' or model_name == 'lsi':
            model = gensim.models.lsimodel.LsiModel(corpus=corpus,
                                                    num_topics=num_topics,
                                                    id2word=id2word,
                                                    chunksize=100)
        # LDA Model
        elif model_name == 'LdaModel' or model_name == 'ldamodel' or model_name == 'lda':
            model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=id2word,
                                                    num_topics=num_topics,
                                                    random_state=100,
                                                    update_every=1,
                                                    chunksize=100,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True)
        # LDAMallet Model
        elif model_name == 'LdaMallet' or model_name == 'ldamallet' or model_name == 'ldamallet':
            model = gensim.models.wrappers.LdaMallet(mallet_path,
                                                     corpus=corpus,
                                                     num_topics=num_topics,
                                                     id2word=id2word)
        else:
            print('Invalid model!')
            return None

        return model

    # Models list and coherence scores list
    model_list, coherence_values = [], []
    # Iterator for max_topics
    iterator = range(start, max_topics + 1, step)

    for num_topics in iterator:
        # Compute models for given max_topics
        computed_model = compute_model(model_name=model_name,
                                       corpus=corpus,
                                       id2word=id2word,
                                       num_topics=num_topics)
        # Append above computed to a list
        model_list.append(computed_model)

        # Compute coherence score for above model
        coherencemodel = CoherenceModel(model=computed_model,
                                        texts=texts,
                                        dictionary=id2word,
                                        coherence=measure)
        # Append above coherence score to a list
        coherence_values.append(coherencemodel.get_coherence())

    # Print all scores to the console
    print('\nCalculating various coherence scores...\n')
    for number_of_topics, score in zip(iterator, coherence_values):
        print(model_name, ": Num Topics =", number_of_topics,
              " Coherence Value :", round(score, 4))

    return model_list, coherence_values
