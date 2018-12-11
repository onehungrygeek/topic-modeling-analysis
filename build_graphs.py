import os
import matplotlib.pyplot as plt


def build_graph(model_name, scores, measure, file_name, limit, time_string, start=5, step=5):
    """
    This module plots all coherence scores on a graph.

    Arguments:
        model {str} -- Model name
        scores {list} -- List of all computed coherence scores
        measure {str} -- Name of the coherence measure used. Possible measures: c_v, c_uci, c_npmi, u_mass
        file_name {str} -- Input file name
        limit {int} -- Maximum number of topics used in computing various coherence scores
        time_string {str} -- Timestamp when code started (for appending to output files)

    Keyword Arguments:
        start {int} -- Start value for x-axis values (default: {5})
        step {int} -- Steps for values on x-axis (default: {5})
    """

    # Get name of dataset by splitting it with .txt extension
    dataset = file_name.split('.')[0]

    # List of all possible model names
    modelname_list = ['LsiModel', 'lsimodel',
                      'LdaModel', 'ldamodel',
                      'LdaMallet', 'ldamallet',
                      'LSI', 'LDA', 'LDAMALLET']
    # Set plot title
    if model_name in modelname_list:
        print(model_name + ' Detected. Generating graph...\n')
        title = dataset + '_' + model_name
    else:
        print('Invalid Model!')
        title = 'ERROR_Graph'

    # List of all possible coherence score names
    coherence_labels = ['c_v', 'c_uci', 'c_npmi', 'u_mass']

    # Set plot label
    if measure in coherence_labels:
        coh_label = measure
    else:
        coh_label = 'ERROR_LABEL'

    # Plot graph
    x = range(start, limit + 1, step)
    plt.plot(x, scores, label=coh_label)
    plt.title(title + ' ' + coh_label + '\n')
    plt.xlabel("Number of topics")
    plt.ylabel("Coherence score")
    # Get current working directory and set output directory
    output_dir = os.getcwd() + '/Output_Files/'
    fig_title = title + '_' + coh_label + '_' + str(limit) + '.png'
    plt.savefig(output_dir + fig_title)
