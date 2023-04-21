import numpy as np
import pandas as pd
from gensim.models import Word2Vec


if __name__ == '__main__':
    mod = Word2Vec.load('/n/henrich_lab/Lab/word2vec/checkpoints/mod_2.model')
    vocab = mod.wv.key_to_index
    print(vocab)

    king = mod.wv.get_vector('king')
    print(king.shape)

    res = mod.wv.most_similar(positive=['king', 'woman'], negative=['man'])
    print(res)
