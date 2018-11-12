import matplotlib.pyplot as plt

def build_graph(model, scores, measure, limit, start=5, step=5):
    if model == 'LsiModel' or model == 'lsimodel':
        print('LSI Model Detected. Generating graph...\n')
        title = 'SPORTS_DATASET_LSI'
    elif model == 'LdaModel' or model == 'ldamodel':
        print('LDA Model Detected. Generating graph...\n')
        title = 'SPORTS_DATASET_LDA'
    elif model == 'LdaMallet' or model == 'ldamallet':
        print('LDA Mallet Model Detected. Generating graph...\n')
        title = 'SPORTS_DATASET_LDA_MALLET'
    else:
        print('Invalid Model!')
        title = 'ERROR_GRAPH'

    if measure == 'c_v':
        coh_label = 'c_v coherence'
    elif measure == 'c_uci':
        coh_label = 'c_uci coherence'
    elif measure == 'c_npmi':
        coh_label = 'c_npmi coherence'
    elif measure == 'u_mass':
        coh_label = 'u_mass coherence'
    else:
        coh_label = 'ERROR_LABEL'

    x = range(start, limit + 1, step)
    plt.plot(x, scores, label=coh_label)
    plt.title(title + ' ' + coh_label + '\n')
    plt.xlabel("Number of topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_scores"), loc='best')
    fig_title = title + '_' + coh_label + '_' + str(limit) + '.png'
    plt.savefig(fig_title)
