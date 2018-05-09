import sys, os, random
import nltk, re
import collections
import time
import pickle
import json

MODEL='data/NaiveBayesClassifier_ngram2_negtnTrue_1000000'
NGRAM_VAL=2
NEGTNVAL=1

def getClassifyData(tweets):
    add_ngram_feat = 2
    add_negtn_feat = 1

    from functools import wraps
    import preprocessing
    procTweets=[]
    for tweet in tweets:
        procTweet=preprocessing.processAll(tweet, subject="", query="")
        procTweets.append(procTweet)

    stemmer = nltk.stem.PorterStemmer()

    all_tweets_pre = []  # DATADICT: all_tweets =   [ (words, sentiment), ... ]
    for text  in procTweets:
        words = [word if (word[0:2] == '__') else word.lower() \
                 for word in text.split() \
                 if len(word) >= 3]
        words = [stemmer.stem(w) for w in words]  # DATADICT: words = [ 'word1', 'word2', ... ]
        all_tweets_pre.append(words)

    unigrams_fd = nltk.FreqDist()
    if add_ngram_feat > 1:
        n_grams_fd = nltk.FreqDist()

    for (words) in all_tweets_pre:
        words_uni = words
        unigrams_fd.update(words)

        if add_ngram_feat >= 2:
            words_bi = [','.join(map(str, bg)) for bg in nltk.bigrams(words)]
            n_grams_fd.update(words_bi)

        if add_ngram_feat >= 3:
            words_tri = [','.join(map(str, tg)) for tg in nltk.trigrams(words)]
            n_grams_fd.update(words_tri)


    if add_ngram_feat > 1:
        sys.stderr.write('\nlen( n_grams ) = ' + str(len(n_grams_fd)))
        ngrams_sorted = [k for (k, v) in n_grams_fd.items() if v > 1]
        sys.stderr.write('\nlen( ngrams_sorted ) = ' + str(len(ngrams_sorted)))

    def get_word_features(words):
        bag = {}
        words_uni = ['has(%s)' % ug for ug in words]

        if (add_ngram_feat >= 2):
            words_bi = ['has(%s)' % ','.join(map(str, bg)) for bg in nltk.bigrams(words)]
        else:
            words_bi = []

        if (add_ngram_feat >= 3):
            words_tri = ['has(%s)' % ','.join(map(str, tg)) for tg in nltk.trigrams(words)]
        else:
            words_tri = []

        for f in words_uni + words_bi + words_tri:
            bag[f] = 1

        # bag = collections.Counter(words_uni+words_bi+words_tri)
        return bag

    negtn_regex = re.compile(r"""(?:
        ^(?:never|no|nothing|nowhere|noone|none|not|
            havent|hasnt|hadnt|cant|couldnt|shouldnt|
            wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
        )$
    )
    |
    n't
    """, re.X)

    def get_negation_features(words):
        INF = 0.0
        negtn = [bool(negtn_regex.search(w)) for w in words]

        left = [0.0] * len(words)
        prev = 0.0
        for i in range(0, len(words)):
            if (negtn[i]):
                prev = 1.0
            left[i] = prev
            prev = max(0.0, prev - 0.1)

        right = [0.0] * len(words)
        prev = 0.0
        for i in reversed(range(0, len(words))):
            if (negtn[i]):
                prev = 1.0
            right[i] = prev
            prev = max(0.0, prev - 0.1)

        return dict(zip(
            ['neg_l(' + w + ')' for w in words] + ['neg_r(' + w + ')' for w in words],
            left + right))

    def extract_features(words):
        features = {}

        word_features = get_word_features(words)
        features.update(word_features)

        if add_negtn_feat:
            negation_features = get_negation_features(words)
            features.update(negation_features)

        #sys.stderr.write('\rfeatures extracted for ' + str(extract_features.count) + ' tweets')
        return features

    extract_features.count = 0;

    v_all=[]
    for tweet_pre in all_tweets_pre:
        v_all.append(extract_features(tweet_pre))
    return (v_all)

def classify(tweets):
    v_all = getClassifyData(tweets)
    filename=MODEL+'.pickle'
    f = open(filename, 'rb')
    classifier_tot = pickle.load(f)
    f.close()
    result = classifier_tot.classify_many(v_all)
    return result

def main(argv):
    data_file_name="twt_SSC.json"
    output_file_name="classified_twt_SSC.json"
    data = json.load(open(data_file_name))
    tweets=[]
    #data = json.load(open('data/qing.json'))
    twts=data["rows"]
    for idx, val in enumerate(twts):
        try:
            tweets.append(val["value"])
        except:
            print idx
    #tweets=tweets[:10]
    sys.stderr.write('\nlen( tweets ) = ' + str(len(tweets)))
    result=classify(tweets)
    for idx, val in enumerate(twts):
        val[unicode('sent', "ascii")]=unicode(result[idx], "ascii")
    with open(output_file_name, 'w') as fp:
        json.dump(twts, fp)
    sys.stdout.flush()

if __name__ == "__main__":
    main(sys.argv[1:])
