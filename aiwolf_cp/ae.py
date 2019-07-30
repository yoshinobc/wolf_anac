import keras
from keras.models import load_model
from keras.models import Model
from keras.datasets import mnist
from keras.layers import Input, Dense
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import pikle

f_train = open("training_data", "rb")
x_train = pickle.load(f_train)

f_test = open("test_data", "rb")
x_test = pickle.load(f_test)

print("x_train: ", x_train.shape)
print("x_test: ", x_test.shape)

# 入力
input_img = Input(shape=(947, ))

# encoder
encoding_dim = 64
encoded = Dense(encoding_dim, activation='relu')(input_img)

# decoder
decoded = Dense(947, activation='sigmoid')(encoded)
autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

print("before training")
expect = autoencoder.predict(x_test, batch_size=256)
print(expect)

# train
autoencoder.fit(x_train, x_train,
                epochs=1000,
                batch_size=256,
                shuffle=True,
                validation_data=(x_valid, x_valid))

print("Finish traning")

print()
print("after training")
# predict
expect = autoencoder.predict(x_test, batch_size=256)
print(expect)
