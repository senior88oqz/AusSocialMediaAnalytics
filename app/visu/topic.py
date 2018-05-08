# coding: utf-8
import couchdb
import gensim
import nltk
import re
import time
# import pickle
import pyLDAvis.gensim
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import wordnet as wn
from gensim import corpora


def get_tweet_re():
    emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""

    regex_str = [
        emoticons_str,
        r'<[^>]+>',  # HTML tags
        r'(?:@[\w_]+)',  # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

        r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'  # anything else
    ]

    tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

    return tokens_re, emoticon_re


def tokenize(s, tokens_re):
    return tokens_re.findall(s)


def preprocess(s, lowercase=True):
    tokens_re, emoticon_re = get_tweet_re()
    tokens = tokenize(s, tokens_re)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


def prepare_text_for_lda(text):
    en_stop = set(nltk.corpus.stopwords.words('english'))
    tokens = preprocess(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens


if __name__ == "__main__":

    start_time = time.time()

    db = couchdb.Server("http://localhost:5984/")['tweets']
    print(db)

    text_data = []
    for item in db.view('_design/allan/_view/content-time', limit=1000):
        token = prepare_text_for_lda(item.value['text'])
        # print(token)
        text_data.append(token)

    print('number of tweets:', len(text_data))

    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]

    # pickle.dump(corpus, open('corpus.pkl', 'wb'))
    # dictionary.save('dictionary.gensim')

    NUM_TOPICS = 10
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS,
                                               id2word=dictionary, passes=15)
    # ldamodel.save('model5.gensim')
    topics = ldamodel.print_topics(num_words=6)
    for topic in topics:
        print(topic)

    # dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
    # corpus = pickle.load(open('corpus.pkl', 'rb'))
    # lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')

    lda_display = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary,
                                          sort_topics=False)
    # pyLDAvis.show(lda_display)
    pyLDAvis.save_html(lda_display, './out/topics.html')
    print("--- %s seconds ---" % (time.time() - start_time))
