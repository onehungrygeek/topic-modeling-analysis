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
import re
import nltk
import spacy
import gensim
import gensim.corpora as corpora
from nltk.corpus import stopwords
from contextlib import redirect_stdout
from gensim.utils import simple_preprocess

# List of English stop words from NLTK library
with redirect_stdout(open(os.devnull, "w")):
    nltk.download("stopwords")
nltk_stop_words = stopwords.words('english')
# List of English stop words from MALLET
with open('mallet_stopwords.txt') as f:
    mallet_stop_words = f.read().splitlines()
# Combined list of English stop words
stop_words = nltk_stop_words + mallet_stop_words


def process_texts(file_name):
    """
    This module preprocesses input text files.
    1. Removes emails, special characters, single quotes.
    2. Removes English stop words from the sentences.
    3. Converts sentences to words and lemmatizes them.

    Arguments:
        file_name {str} -- Input text file name

    Returns:
        list -- List of words ready to be converted into corpus
    """

    # Open input text file and readlines
    with open(file_name) as f:
        train_text = f.readlines()
    train_text = [x.strip() for x in train_text]

    # Remove Emails
    train_text = [re.sub('\S*@\S*\s?', '', sent) for sent in train_text]
    # Remove new line characters
    train_text = [re.sub('\s+', ' ', sent) for sent in train_text]
    # Remove distracting single quotes
    train_text = [re.sub("\'", "", sent) for sent in train_text]

    def sentence_to_words(sentences):
        """
        Convert sentences to words using gensim's simple_preprocess module.

        Arguments:
            sentences {list} -- List of training texts
        """

        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

    def remove_stopwords(texts):
        """
        Remove words from stop_words list

        Arguments:
            texts {list} -- List of data words

        Returns:
            list -- List of words with stop words removed
        """

        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    def make_bigrams(texts):
        """
        Create bigrams from all words list.
        For example, 'police' and 'station' will be combined as one bigram 'police_station'.

        Arguments:
            texts {list} -- List of data words without stop words

        Returns:
            list -- List of data words with their possible bigrams
        """

        return [bigram_mod[doc] for doc in texts]

    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        """
        Lemmatization takes into consideration the morphological analysis of the words.
        For example, 'studies' and 'studying' are both converted to their lemma as 'study'.

        Arguments:
            texts {list} -- List of data words and bigrams with stop words removed

        Keyword Arguments:
            allowed_postags {list} -- List of allowed postags for English language lemmatization
                                        (default: {['NOUN', 'ADJ', 'VERB', 'ADV']})

        Returns:
            list -- List of completely preprocessed data words
        """

        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent))
            texts_out.append(
                [token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    data_words = list(sentence_to_words(train_text))
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    data_words_nostops = remove_stopwords(data_words)
    data_words_bigrams = make_bigrams(data_words_nostops)
    # Load English language module from spacy
    nlp = spacy.load('en', disable=['parser', 'ner'])
    data_lemmatized = lemmatization(data_words_bigrams)

    return data_lemmatized
