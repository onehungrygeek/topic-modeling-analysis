import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
from gensim.models import CoherenceModel


def compute_coherence(model, texts, dictionary, measure):
    # if modelname == 'lsimodel' or modelname == 'LsiModel':
    #     model = lsimodel
    # elif modelname == 'HdpModel' or modelname == 'hdpmodel':
    #     model = hdpmodel
    # elif modelname == 'LdaModel' or modelname == 'ldamodel':
    #     model = ldamodel
    # elif modelname == 'LDAMallet' or modelname == 'ldamallet':
    #     model = ldamallet
    coherence_model = CoherenceModel(model=model,
                                     texts=texts,
                                     dictionary=dictionary,
                                     coherence=measure)
    coherence_score = coherence_model.get_coherence()

    return coherence_model, coherence_score

# def compute_all_scores(model, corpus, id2word, texts, limit, start=5, step=5):
#     coherence_values = []
#     model_list = []
#     for num_topics in range(start, limit, step):
#         model, topics = compute_model(model, corpus, id2word)
#         # model = gensim.models.wrappers.LdaMallet(mallet_path,
#         #                                          corpus=corpus,
#         #                                          num_topics=num_topics,
#         #                                          id2word=id2word)
#         model_list.append(model)
#         coherencemodel = CoherenceModel(model=model,
#                                         texts=texts,
#                                         dictionary=id2word,
#                                         coherence='c_v')
#         coherence_values.append(coherencemodel.get_coherence())
#
#     return model_list, coherence_values
