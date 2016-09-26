#
# Based on the LSTM/RNN Tutorial on Keras
#

import os
os.environ["THEANO_FLAGS"] = "mode=FAST_RUN,device=gpu,floatX=float32"

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys


text = open('corpora.txt').read().lower()
print('corpus length:', len(text))

chars        = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

print('total chars:', len(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen     = 20
step       = 3
sentences  = []
next_chars = []

for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])

print('nb sequences:', len(sentences))

print('Vectorization')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1



# build the model: a single LSTM
print('Building Model')
model = Sequential()
model.add(LSTM(256, input_shape=(maxlen, len(chars)),return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    
    # helper function to sample an index from a probability array
    preds     = np.asarray(preds).astype('float64')
    preds     = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds     = exp_preds / np.sum(exp_preds)
    probas    = np.random.multinomial(1, preds, 1)
    
    return np.argmax(probas)


# train the model and output the character sequence for 30 iterations
for iteration in range(1, 30):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=128, nb_epoch=1)

    start_index = random.randint(0, len(text) - maxlen - 1)

    for diversity in [0.5]:
        print()
        print('diversity:', diversity)

        generated  = ''
        sentence   = text[start_index: start_index + maxlen]
        generated += sentence
        print('Seed Sequence: "' + sentence + '"')
        sys.stdout.write(generated)

        for i in range(400):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.

            preds      = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char  = indices_char[next_index]

            generated += next_char
            sentence   = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()






