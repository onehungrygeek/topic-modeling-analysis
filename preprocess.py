import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
import gensim.corpora as corpora
import gensim
import spacy
import nltk
import re
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess

stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])


def process_texts(file_name):
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
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

    data_words = list(sentence_to_words(train_text))

    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]

    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent))
            texts_out.append(
                [token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    data_words_nostops = remove_stopwords(data_words)
    data_words_bigrams = make_bigrams(data_words_nostops)
    nlp = spacy.load('en', disable=['parser', 'ner'])
    data_lemmatized = lemmatization(data_words_bigrams,
                                    allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    return data_lemmatized
