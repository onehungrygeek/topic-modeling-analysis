# Library imports
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=DeprecationWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=DeprecationWarning)
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
import time
import pandas as pd
import numpy as np
import gensim.corpora as corpora
from subprocess import Popen as notifyThis
from pprint import pprint

# My module imports
from preprocess import process_texts
from compute_models import compute_model
from visualize_ldamodel import visualize
from compute_coherence_score import compute_coherence
from compute_all_coherence_scores import compute_all_scores
from optimal_topics import print_optimal_topics
from build_graphs import build_graph
from compute_sentence_wise_topics import compute_sentence_wise_topics


def run_topic_model():
    time_string = time.strftime("%m-%d-%Y_%H-%M-%S")

    # Notification system for Ubuntu 18.04
    def notifier(icon, title, message=''):
        try:
            notifyThis(
                ['notify-send',
                 '--icon=/home/akshay/Rest/Practice/topic-model-temp/notify-icons/' + icon + '.png',
                 title,
                 message])
        except:
            pass

    notifier('analysis', 'Starting topic model analysis...',
             'Please enter input text file name in console.')
    # Preprocess input text file
    file_name = input('Enter text file name for analysis:\t')
    data_lemmatized = process_texts(file_name)
    id2word = corpora.Dictionary(data_lemmatized)
    texts = data_lemmatized
    corpus = [id2word.doc2bow(text) for text in texts]

    notifier('preprocess', 'Text preprocessing complete!')

    num_topics = 5
    # Develop all models and respective topics
    lsimodel, lsitopics = compute_model(
        'lsimodel', corpus, id2word, num_topics=num_topics)
    print('\nLSI Topics\n')
    pprint(lsitopics)

    hdpmodel, hdptopics = compute_model(
        'hdpmodel', corpus, id2word, num_topics=num_topics)
    print('\nHDP Topics\n')
    pprint(hdptopics)

    ldamodel, ldatopics = compute_model(
        'ldamodel', corpus, id2word, num_topics=num_topics)
    print('\nLDA Topics\n')
    pprint(ldatopics)

    ldamallet, ldamallettopics = compute_model(
        'ldamallet', corpus, id2word, num_topics=num_topics)
    print('\nLDA MALLET Topics\n')
    pprint(ldamallettopics)

    # Visualize LDA model and save as .html file
    visualize(ldamodel, corpus, id2word, time_string)

    notifier('models', 'All models developed successfully!', 'LDA visualization HTML for ' +
             str(num_topics) + ' topics saved to Output_Files directory.')

    # Compute coherence for above developed models
    lsi_coherence, lsi_score = compute_coherence(
        lsimodel, data_lemmatized, id2word, 'c_v')
    hdp_coherence, hdp_score = compute_coherence(
        hdpmodel, data_lemmatized, id2word, 'c_v')
    lda_coherence, lda_score = compute_coherence(
        ldamodel, data_lemmatized, id2word, 'c_v')
    ldamallet_coherence, ldamallet_score = compute_coherence(
        ldamallet, data_lemmatized, id2word, 'c_v')

    notifier('scores', 'Coherence scores determined!',
             'Check console for model coherence scores.')

    print('\nLSI Coherence Score:', lsi_score)
    print('\nHDP Coherence Score:', hdp_score)
    print('\nLDA Coherence Score:', lda_score)
    print('\nLDA Mallet Coherence Score:', ldamallet_score)

    print()

    # Run analysis to find coherence scores for different models with increasing num of topics
    max_topics = 50

    notifier('scores', 'Analyzing various coherence scores for upto ' + str(max_topics) +
             ' topics...', 'Sit back and relax as this analysis may take several minutes to complete.')

    lsi_list, lsi_all_scores = compute_all_scores(modelname='lsimodel',
                                                  corpus=corpus,
                                                  id2word=id2word,
                                                  texts=data_lemmatized,
                                                  measure='c_v',
                                                  limit=max_topics)
    print('\nOptimal LSI Topics\n')
    print_optimal_topics(model_list=lsi_list,
                         all_scores=lsi_all_scores)

    lda_list, lda_all_scores = compute_all_scores(modelname='ldamodel',
                                                  corpus=corpus,
                                                  id2word=id2word,
                                                  texts=data_lemmatized,
                                                  measure='c_v',
                                                  limit=max_topics)
    print('\nOptimal LDA Topics\n')
    print_optimal_topics(model_list=lda_list,
                         all_scores=lda_all_scores)

    ldamallet_list, ldamallet_all_scores = compute_all_scores(modelname='ldamallet',
                                                              corpus=corpus,
                                                              id2word=id2word,
                                                              texts=data_lemmatized,
                                                              measure='c_v',
                                                              limit=max_topics)
    print('\nOptimal LDA MALLET Topics\n')
    print_optimal_topics(model_list=ldamallet_list,
                         all_scores=ldamallet_all_scores)

    print()

    notifier('scores', 'Coherence score analysis complete!',
             'Check console to find optimal model topics.')

    # Build graphs using above calculated coherence scores
    build_graph(model='lsimodel',
                scores=lsi_all_scores,
                measure='c_v',
                file_name=file_name,
                limit=max_topics,
                time_string=time_string)

    build_graph(model='ldamodel',
                scores=lda_all_scores,
                measure='c_v',
                file_name=file_name,
                limit=max_topics,
                time_string=time_string)

    build_graph(model='ldamallet',
                scores=ldamallet_all_scores,
                measure='c_v',
                file_name=file_name,
                limit=max_topics,
                time_string=time_string)

    notifier('graphs', 'Graphs built successfully!',
             'Check Output_Files directory for saved graphs.')

    # Place senteces from input file to their respective topics and save to .csv file
    df_lda_sentence_wise_topics, dominant_sentence_in_topics_lda = compute_sentence_wise_topics(
        modelname='LDA', model=ldamodel, corpus=corpus, file_name=file_name, time_string=time_string)
    df_lsi_sentence_wise_topics, dominant_sentence_in_topics_lsi = compute_sentence_wise_topics(
        modelname='LSI', model=lsimodel, corpus=corpus, file_name=file_name, time_string=time_string)
    df_ldamallet_sentence_wise_topics, dominant_sentence_in_topics_ldamdallet = compute_sentence_wise_topics(
        modelname='LDAMallet', model=ldamallet, corpus=corpus, file_name=file_name, time_string=time_string)

    notifier('complete', 'Topic model analysis complete!',
             'Check Output_Files directory for saved csv files.')


if __name__ == '__main__':
    run_topic_model()
