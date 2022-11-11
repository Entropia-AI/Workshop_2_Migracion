import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer


def get_n_grams(srs_texts, n_gram=2, n_top=100):

    # Initialize and count vectorize the docs
    count_vect = CountVectorizer(min_df=2, max_df=0.95,
                                 ngram_range=(n_gram, n_gram))
    word_count_vector = count_vect.fit_transform(srs_texts)

    # Extract ngrams
    feature_names = count_vect.get_feature_names()

    # Get the absolute frequency
    terms_frec = {}
    for name in feature_names:
        index_name = feature_names.index(name)
        s = np.sum(word_count_vector[:, index_name])
        terms_frec[name] = s.item()

    # Get the N-Top ngrams
    ngrams_dict = dict(sorted(terms_frec.items(),
                              reverse=True,
                              key=lambda x: x[1]))

    ngrams_list = list(ngrams_dict.items())
    top_ngrams = ngrams_list[:n_top]

    df_ngrams = pd.DataFrame(top_ngrams)
    df_ngrams.columns = ['n_gram', 'total_freq']

    return df_ngrams
