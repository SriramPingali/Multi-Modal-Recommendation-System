import re
import numpy as np

from keras.optimizers import Adam
from keras.models import Model, Sequential

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.stem import wordnet
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize as wt

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.losses import sparse_categorical_crossentropy
from keras.layers import LSTM, Input, TimeDistributed, Dense, Activation, RepeatVector, Embedding, Bidirectional

lem = wordnet.WordNetLemmatizer()
sw = set(stopwords.words("english"))

class Autoencoder_Text(Model):
    def __init__(self, input_=300, hidden=200, vocab = 13672):
        super(Autoencoder_Text, self).__init__()
        self.max_len = input_
        self.hidden = hidden
        self.vocab = vocab

    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r"@[A-Za-z0-9]+", ' ', text)
        text = re.sub(r"https?://[A-Za-z0-9./]+", ' ', text)
        text = re.sub(r"[^a-zA-z.!?'0-9]", ' ', text)
        text = re.sub('\t', ' ',  text)
        text = re.sub(r" +", ' ', text)
        text = wt(text)
        text = (" ").join([lem.lemmatize(i, pos ='v')
                           for i in text if i not in sw])
        return(text)

    def tokenize(self, sentences):
        text_tokenizer = Tokenizer()
        text_tokenizer.fit_on_texts(sentences)
        return(text_tokenizer.texts_to_sequences(sentences), text_tokenizer)

    def pre_process(self, data_text, train=False):
        data_text = data_text.apply(self.clean_text)
        text_tokenized, self.text_tokenizer = self.tokenize(data_text)

        if train:
            self.vocab = len(self.text_tokenizer.word_index) + 1
            self.max_len = int(len(max(text_tokenized,key=len)))

        pad_sentence = pad_sequences(text_tokenized, self.max_len, padding = "post")
        return(pad_sentence.reshape(*pad_sentence.shape, 1))

    def model(self):
        self.encoder = Sequential([
            Embedding(input_dim = self.vocab, output_dim=128,),
            Bidirectional(LSTM(self.hidden, return_sequences=False))
        ])

        self.r_vec = RepeatVector(self.max_len)
        self.decoder = Sequential([
            Bidirectional(LSTM(self.hidden, return_sequences=True, dropout=0.2)),
            TimeDistributed(Dense(self.vocab))
        ])
        self.enc_dec_model = Sequential([self.encoder, self.r_vec, self.decoder])

    def train(self, data_text, epochs=10, batch_size=20):
        pad_sentence = self.pre_process(data_text, True)
        self.model()
        self.enc_dec_model.compile(loss=sparse_categorical_crossentropy,
              optimizer=Adam(1e-3),
              metrics=['accuracy'])

        self.enc_dec_model.summary()
        self.enc_dec_model.fit(np.squeeze(pad_sentence, axis = 2),
                                      pad_sentence, batch_size=batch_size, epochs=epochs)
        self.enc_dec_model.save('./pretrained/text_model')

    def call(self, inputs):
        pad_sentences = self.pre_process(inputs, False)
        print(tf.convert_to_tensor(pad_sentences).shape)
        return(self.enc_dec_model(tf.squeeze(pad_sentences, axis = 2)))
