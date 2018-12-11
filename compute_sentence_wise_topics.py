import os
import pandas as pd
import numpy as np
import time


def compute_sentence_wise_topics(modelname, model, corpus, file_name, time_string):
    """
    This module corresponds sentences from the input file to their dominant topics from the model analysis.

    Arguments:
        modelname {str} -- Name of the model
        model {gensim.models.MODEL} -- Input gensim model
        corpus {list} -- List of corpus created from preprocessed texts
        file_name {} -- Input file name
        time_string {str} -- Timestamp when code started (for appending to output files)
    """

    # Create a pandas dataframe
    df_output = pd.DataFrame()

    # Rearrange rows from gensim model dictionary according to the topic
    # dominance to get dominant topic in each sentence, get respective
    # keywords and topic number and append it to the df_output dataframe.
    for i, row in enumerate(model[corpus]):
        try:
            row = sorted(row[0], key=lambda x: (x[1]), reverse=True)
        except:
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:
                wp = model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                df_output = df_output.append(pd.Series([int(topic_num),
                                                        round(prop_topic * 100, 2),
                                                        topic_keywords]),
                                             ignore_index=True)
            else:
                break

    # Set column names
    df_output.columns = ['Dominant_Topic_Number',
                         'Percentage_Contribution', 'Keywords_In_Dominant_Topic']

    # Convert sentences in input file to a column
    df_base_sentences = pd.read_table(file_name, header=None)

    # Append above dataframe column to output dataframe
    df_output['Sentences'] = df_base_sentences[0]

    # Rearrange columns in proper order
    df_output = df_output[['Dominant_Topic_Number', 'Percentage_Contribution',
                           'Keywords_In_Dominant_Topic', 'Sentences']]

    # Append % sign
    df_output['Percentage_Contribution'] = (
        df_output.Percentage_Contribution).astype(str) + ' %'

    # Reset index
    df_output = df_output.reset_index()

    # Set name of the index column to Line_Number
    df_output.rename(columns={'index': 'Line_Number'}, inplace=True)

    # Set Line_Number column as the index
    df_output.set_index('Line_Number', inplace=True)

    # Convert topic number from float to int
    df_output['Dominant_Topic_Number'] = df_output['Dominant_Topic_Number'].astype(
        np.int64)

    # Normal Save
    # Save pandas dataframe to a csv file in Output_Files directory
    # Note: Please create this directory if it does not exist
    output_dir = os.getcwd() + '/Output_Files/'
    csv_file_name = file_name.split('.')[0] + '_' + \
        modelname + '_' + time_string + '.csv'
    print('\nSaving current sentence wise analysis of model to: ',
          output_dir + csv_file_name)
    df_output.to_csv(output_dir + csv_file_name, encoding='utf-8')

    # Sorted Save
    # Sort based on the topic number
    df_output = df_output.sort_values('Dominant_Topic_Number')
    # Save pandas dataframe to a csv file
    sorted_csv_file_name = 'SORTED_' + csv_file_name
    print('\nSaving SORTED current sentence wise analysis of model to: ',
          output_dir + sorted_csv_file_name)
    df_output.to_csv(output_dir + sorted_csv_file_name, encoding='utf-8')

    # Dominant sentence for each topic
    dominant_sentence_in_topics = pd.DataFrame()

    sent_topics_outdf_grpd = df_output.groupby('Dominant_Topic_Number')

    for i, grp in sent_topics_outdf_grpd:
        dominant_sentence_in_topics = pd.concat([dominant_sentence_in_topics,
                                                 grp.sort_values(['Percentage_Contribution'], ascending=[0]).head(1)],
                                                axis=0)

    # Reset Index
    dominant_sentence_in_topics.reset_index(drop=True, inplace=True)

    dominant_sentence_in_topics.columns = [
        'Topic_Number', "Sentence_Percentage_Contribution", "Topic_Keywords", "Sentences"]

    dominant_file_name = 'dominant_sentences_' + csv_file_name
    print('\nSaving dominant sentence per topic csv file to: ',
          output_dir + dominant_file_name)
    dominant_sentence_in_topics.to_csv(
        output_dir + dominant_file_name, encoding='utf-8')
