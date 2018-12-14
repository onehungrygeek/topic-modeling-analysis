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
from gensim.models import CoherenceModel


def compute_coherence(model, texts, dictionary, measure):
    """
    This module computes coherence score for a given model

    Arguments:
        model {gensim.models.MODEL} -- Input gensim model
        texts {list} -- List of preprocessed input words
        dictionary {Dictionary} -- Dictionary of ids with mapped words
        measure {str} -- Name of the coherence measure you want to use. Possible measures: c_v, c_uci, c_npmi, u_mass

    Returns:
        float -- Calculated coherence score for given model
    """

    coherence_model = CoherenceModel(model=model,
                                     texts=texts,
                                     dictionary=dictionary,
                                     coherence=measure)
    coherence_score = coherence_model.get_coherence()

    return coherence_score
