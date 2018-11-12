import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
from gensim.models import CoherenceModel


def compute_coherence(model, texts, dictionary, measure):
    coherence_model = CoherenceModel(model=model,
                                     texts=texts,
                                     dictionary=dictionary,
                                     coherence=measure)
    coherence_score = coherence_model.get_coherence()

    return coherence_model, coherence_score
