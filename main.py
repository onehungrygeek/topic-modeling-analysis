import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
import numpy as np
import pandas as pd
import gensim.corpora as corpora
import preprocess
from compute_models import compute_model
# from pprint import pprint
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from compute_coherence_score import compute_coherence
from compute_all_coherence_scores import compute_all_scores
from build_graphs import build_graph


def run_topic_model():
    file_name = 'sports.txt'
    data_lemmatized = preprocess.process_texts(file_name)
    id2word = corpora.Dictionary(data_lemmatized)
    texts = data_lemmatized
    corpus = [id2word.doc2bow(text) for text in texts]

    lsimodel, lsitopics = compute_model('lsimodel', corpus, id2word)
    print('\nLSI Topics\n', lsitopics)
    hdpmodel, hdptopics = compute_model('hdpmodel', corpus, id2word)
    print('\nHDP Topics\n', hdptopics)
    ldamodel, ldatopics = compute_model('ldamodel', corpus, id2word)
    print('\nLDA Topics\n', ldatopics)
    ldamallet, ldamallettopics = compute_model('ldamallet', corpus, id2word)
    print('\nLDA MALLET Topics\n', ldamallettopics)

    lsi_coherence, lsi_score = compute_coherence(
        lsimodel, data_lemmatized, id2word, 'c_v')
    hdp_coherence, hdp_score = compute_coherence(
        hdpmodel, data_lemmatized, id2word, 'c_v')
    lda_coherence, lda_score = compute_coherence(
        ldamodel, data_lemmatized, id2word, 'c_v')
    ldamallet_coherence, ldamallet_score = compute_coherence(
        ldamallet, data_lemmatized, id2word, 'c_v')

    print('\nLSI Coherence Score:', lsi_score)
    print('\nHDP Coherence Score:', hdp_score)
    print('\nLDA Coherence Score:', lda_score)
    print('\nLDA Mallet Coherence Score:', ldamallet_score)

    limit = 15
    x = range(5, limit + 1, 5)
    lsi_list, lsi_all_scores = compute_all_scores(modelname='lsimodel',
                                                  corpus=corpus,
                                                  id2word=id2word,
                                                  texts=data_lemmatized,
                                                  measure='c_v',
                                                  limit=limit)

    # print(lsi_all_scores)
    # print(optimal_lsi_idx)

    # for n, score in zip(x, lsi_all_scores):
    #     print("LSI Num Topics =", n, " has Coherence Value of", round(score, 4))

    optimal_lsi_idx = np.argmax(lsi_all_scores)
    # optimal_lsi_idx = lsi_list.index(max(lsi_all_scores))
    optimal_lsimodel = lsi_list[optimal_lsi_idx]
    optimal_lsi_topics = optimal_lsimodel.show_topics(formatted=False)
    print('\nOptimal LSI Topics\n', optimal_lsimodel.print_topics())
    # Can add num_words = 10 to above print_topics() function

    lda_list, lda_all_scores = compute_all_scores(modelname='ldamodel',
                                                  corpus=corpus,
                                                  id2word=id2word,
                                                  texts=data_lemmatized,
                                                  measure='c_v',
                                                  limit=limit)
    # print(lda_all_scores)
    # for n, score in zip(x, lda_all_scores):
    #     print("Num Topics =", n, " has Coherence Value of", round(score, 4))

    # optimal_lda_idx = lda_list.index(max(lda_all_scores))
    optimal_lda_idx = np.argmax(lda_all_scores)
    optimal_ldamodel = lda_list[optimal_lda_idx]
    optimal_lda_topics = optimal_ldamodel.show_topics(formatted=False)
    print('\nOptimal LDA Topics\n', optimal_ldamodel.print_topics())

    ldamallet_list, ldamallet_all_scores = compute_all_scores(modelname='ldamallet',
                                                              corpus=corpus,
                                                              id2word=id2word,
                                                              texts=data_lemmatized,
                                                              measure='c_v',
                                                              limit=limit)

    optimal_ldamallet_idx = np.argmax(ldamallet_all_scores)
    optimal_ldamallet_model = lda_list[optimal_ldamallet_idx]
    optimal_ldamallet_topics = optimal_ldamallet_model.show_topics(formatted=False)
    print('\nOptimal LDA MALLET Topics\n', optimal_ldamallet_model.print_topics())

    build_graph(model='lsimodel',
                scores=lsi_all_scores,
                measure='c_v',
                limit=limit)


if __name__ == '__main__':
    run_topic_model()
