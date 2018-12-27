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
import time
import numpy as np
import pandas as pd
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


def analyze_topic_models():
    """
    Topic Modeling Module

    Arguments:
        None

    Returns:
        None
    """

    # Get current timestamp to add it to all the output file names
    time_string = time.strftime("%m-%d-%Y_%H-%M-%S")

    def notifier(icon, title, message=''):
        """
        My custom notification system for Ubuntu 18.04
        * Ignore this if you have any other system than Ubuntu 18.04 *

        Arguments:
            icon {str} -- Icon file name saved in notify-icons directory (without .png extension)
            title {str} -- Title for the notification

        Keyword Arguments:
            message {str} -- Message body for the notification (default: {''})
        """
        try:
            current_dir = os.getcwd()
            notifyThis(['notify-send',
                        '--icon=' + current_dir + '/notify-icons/' + icon + '.png',
                        title,
                        message])
        except:
            pass

    # Notification: Topic modeling started
    notifier(icon='analysis',
             title='Starting topic model analysis...',
             message='Please enter input text file name in console.')

    # Receive input for file name
    file_name = input('Enter text file name for analysis:\t')
    # Preprocess the input text file
    data_lemmatized = process_texts(file_name)
    # Compute id2word dictionary from gensim's corpora module
    id2word = corpora.Dictionary(data_lemmatized)
    # Create copy of data_lemmatized so that we can keep the original
    texts = data_lemmatized
    # To develop all models, create a corpus by converting documents from texts to bag of words
    corpus = [id2word.doc2bow(text) for text in texts]

    # Notification: Preprocessing complete
    notifier(icon='preprocess',
             title='Text preprocessing complete!')

    # Develop all models and respective topics
    # Declare how many topics do you want the models to compute
    # Note: HDP does not require num_topics because it computes all possible number of topics in given input
    num_topics = 5
    # LSI Model and Topics
    lsimodel, lsitopics = compute_model(model_name='lsi',
                                        corpus=corpus,
                                        id2word=id2word,
                                        num_topics=num_topics)
    print('\nLSI Topics\n')
    pprint(lsitopics)

    # HDP Model and Topics
    hdpmodel, hdptopics = compute_model(model_name='hdp',
                                        corpus=corpus,
                                        id2word=id2word,
                                        num_topics=num_topics)
    print('\nHDP Topics\n')
    pprint(hdptopics)

    # LDA Model and Topics
    ldamodel, ldatopics = compute_model(model_name='lda',
                                        corpus=corpus,
                                        id2word=id2word,
                                        num_topics=num_topics)
    print('\nLDA Topics\n')
    pprint(ldatopics)

    # LDAMallet Model and Topics
    ldamallet, ldamallettopics = compute_model(model_name='ldamallet',
                                               corpus=corpus,
                                               id2word=id2word,
                                               num_topics=num_topics)
    print('\nLDA MALLET Topics\n')
    pprint(ldamallettopics)

    # Visualize LDA model and save as .html file to Output_Files directory
    # Note: Only LDA model can be visualized using pyLDAvis library.
    visualize(model=ldamodel,
              corpus=corpus,
              id2word=id2word,
              time_string=time_string)

    # Notification: Models developed
    notifier(icon='models',
             title='All models developed successfully!',
             message='LDA visualization HTML for ' + str(num_topics) + ' topics saved to Output_Files directory.')

    # Compute coherence score for above developed models
    # LSI Coherence Score
    lsi_score = compute_coherence(model=lsimodel,
                                  texts=data_lemmatized,
                                  dictionary=id2word,
                                  measure='c_v')

    # HDP Coherence Score (Irrelevant)
    hdp_score = compute_coherence(model=hdpmodel,
                                  texts=data_lemmatized,
                                  dictionary=id2word,
                                  measure='c_v')

    # LDA Coherence Score
    lda_score = compute_coherence(model=ldamodel,
                                  texts=data_lemmatized,
                                  dictionary=id2word,
                                  measure='c_v')

    # LDAMallet Coherence Score
    ldamallet_score = compute_coherence(model=ldamallet,
                                        texts=data_lemmatized,
                                        dictionary=id2word,
                                        measure='c_v')

    # Notification: Computed coherence scores
    notifier(icon='scores',
             title='Coherence scores determined!',
             message='Check console for model coherence scores.')

    # Print computed coherence scores
    print('\nLSI Coherence Score:', lsi_score)
    print('\nHDP Coherence Score:', hdp_score)
    print('\nLDA Coherence Score:', lda_score)
    print('\nLDA Mallet Coherence Score:', ldamallet_score)

    print()

    # Run analysis to find coherence scores for different models with increasing num of topics
    # Note: Cannot run this analysis for HDP because it does not accept num_topics parameter
    max_topics = 50

    # Notification: Coherence score analysis started
    notifier(icon='scores',
             title='Analyzing various coherence scores for upto ' + str(max_topics) +
             ' topics...',
             message='Sit back and relax as this analysis may take several minutes to complete.')

    # Optimal LSI Topics
    print('\nOptimal LSI Topics\n')
    lsi_list, lsi_all_scores = compute_all_scores(model_name='lsimodel',
                                                  corpus=corpus,
                                                  id2word=id2word,
                                                  texts=data_lemmatized,
                                                  measure='c_v',
                                                  max_topics=max_topics)
    print_optimal_topics(model_list=lsi_list,
                         all_scores=lsi_all_scores)

    # Optimal LDA Topics
    print('\nOptimal LDA Topics\n')
    lda_list, lda_all_scores = compute_all_scores(model_name='ldamodel',
                                                  corpus=corpus,
                                                  id2word=id2word,
                                                  texts=data_lemmatized,
                                                  measure='c_v',
                                                  max_topics=max_topics)
    print_optimal_topics(model_list=lda_list,
                         all_scores=lda_all_scores)

    # Optimal LDAMallet Topics
    print('\nOptimal LDA MALLET Topics\n')
    ldamallet_list, ldamallet_all_scores = compute_all_scores(model_name='ldamallet',
                                                              corpus=corpus,
                                                              id2word=id2word,
                                                              texts=data_lemmatized,
                                                              measure='c_v',
                                                              max_topics=max_topics)
    print_optimal_topics(model_list=ldamallet_list,
                         all_scores=ldamallet_all_scores)

    print()

    # Notification: Coherence score analysis complete
    notifier(icon='scores',
             title='Coherence score analysis complete!',
             message='Check console to find optimal model topics.')

    # Build plots using above calculated coherence scores
    # LSI Graph
    build_graph(model_name='LSI',
                scores=lsi_all_scores,
                measure='c_v',
                file_name=file_name,
                limit=max_topics,
                time_string=time_string)

    # LDA Graph
    build_graph(model_name='LDA',
                scores=lda_all_scores,
                measure='c_v',
                file_name=file_name,
                limit=max_topics,
                time_string=time_string)

    # LDAMallet Graph
    build_graph(model_name='LDAMALLET',
                scores=ldamallet_all_scores,
                measure='c_v',
                file_name=file_name,
                limit=max_topics,
                time_string=time_string)

    # Notification: Graphs built
    notifier(icon='graphs',
             title='Graphs built successfully!',
             message='Check Output_Files directory for saved graphs.')

    # Correspond input sentences to their dominant topics and save outputs as .csv files
    # LSI
    compute_sentence_wise_topics(model_name='LSI',
                                 model=lsimodel,
                                 corpus=corpus,
                                 file_name=file_name,
                                 time_string=time_string)
    # LDA
    compute_sentence_wise_topics(model_name='LDA',
                                 model=ldamodel,
                                 corpus=corpus,
                                 file_name=file_name,
                                 time_string=time_string)
    # LDAMallet
    compute_sentence_wise_topics(model_name='LDAMallet',
                                 model=ldamallet,
                                 corpus=corpus,
                                 file_name=file_name,
                                 time_string=time_string)

    # Notification: Topic modeling ended
    notifier(icon='complete',
             title='Topic model analysis complete!',
             message='Check Output_Files directory for saved csv files.')

    with open('/Output_Files/topics_keywords_scores_' + time_string + '.txt', 'w') as file:
        write_this_to_file = ['LSI Topics', lsitopics,
                              'HSP Topics', hdptopics,
                              'LDA Topics', ldatopics,
                              'LDA MALLET Topics', ldamallettopics,
                              'LSI Coherence Score:', lsi_score,
                              'HDP Coherence Score:', hdp_score,
                              'LDA Coherence Score:', lda_score,
                              'LDA Mallet Coherence Score:', ldamallet_score]
        for string in write_this_to_file:
            pprint(string, file)

        print('\nSaving topics, keywords and coherences scores for computed models with ' + str(num_topics) +
              ' topics to Output_Files directory as: ' + 'topics_keywords_scores_' + time_string + '\n')


if __name__ == '__main__':
    analyze_topic_models()
