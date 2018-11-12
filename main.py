import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
import preprocess
import gensim.corpora as corpora
import pandas as pd
import numpy as np
from optimal_topics import print_optimal_topics
from build_graphs import build_graph
from compute_all_coherence_scores import compute_all_scores
from compute_coherence_score import compute_coherence
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
from compute_models import compute_model
from pprint import pprint


def run_topic_model():
    file_name = 'sports.txt'
    data_lemmatized = preprocess.process_texts(file_name)
    id2word = corpora.Dictionary(data_lemmatized)
    texts = data_lemmatized
    corpus = [id2word.doc2bow(text) for text in texts]

    lsimodel, lsitopics = compute_model('lsimodel', corpus, id2word)
    print('\nLSI Topics\n')
    pprint(lsitopics)

    hdpmodel, hdptopics = compute_model('hdpmodel', corpus, id2word)
    print('\nHDP Topics\n')
    pprint(hdptopics)

    ldamodel, ldatopics = compute_model('ldamodel', corpus, id2word)
    print('\nLDA Topics\n')
    pprint(ldatopics)

    ldamallet, ldamallettopics = compute_model('ldamallet', corpus, id2word)
    print('\nLDA MALLET Topics\n')
    pprint(ldamallettopics)

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

    limit = 50
    x = range(5, limit + 1, 5)
    lsi_list, lsi_all_scores = compute_all_scores(modelname='lsimodel',
                                                  corpus=corpus,
                                                  id2word=id2word,
                                                  texts=data_lemmatized,
                                                  measure='c_v',
                                                  limit=limit)
    print('\nOptimal LSI Topics\n')
    print_optimal_topics(model_list=lsi_list,
                         all_scores=lsi_all_scores)

    lda_list, lda_all_scores = compute_all_scores(modelname='ldamodel',
                                                  corpus=corpus,
                                                  id2word=id2word,
                                                  texts=data_lemmatized,
                                                  measure='c_v',
                                                  limit=limit)
    print('\nOptimal LDA Topics\n')
    print_optimal_topics(model_list=lda_list,
                         all_scores=lda_all_scores)

    ldamallet_list, ldamallet_all_scores = compute_all_scores(modelname='ldamallet',
                                                              corpus=corpus,
                                                              id2word=id2word,
                                                              texts=data_lemmatized,
                                                              measure='c_v',
                                                              limit=limit)
    print('\nOptimal LDA MALLET Topics\n')
    print_optimal_topics(model_list=ldamallet_list,
                         all_scores=ldamallet_all_scores)

    build_graph(model='lsimodel',
                scores=lsi_all_scores,
                measure='c_v',
                limit=limit)

    build_graph(model='ldamodel',
                scores=lda_all_scores,
                measure='c_v',
                limit=limit)

    build_graph(model='ldamallet',
                scores=ldamallet_all_scores,
                measure='c_v',
                limit=limit)


if __name__ == '__main__':
    run_topic_model()
