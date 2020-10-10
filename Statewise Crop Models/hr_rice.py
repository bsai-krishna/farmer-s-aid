
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error 
import tensorflow as tf


from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score

from sklearn.pipeline import Pipeline
import pickle

# %matplotlib inline



path = r"C:\Users\anush\OneDrive\Desktop\SIH-Project-Central-Crew\Utils\Final processed csv files\Haryana_Rice.csv"
df = pd.read_csv(path)

df['District'].unique()

df['District_encode'] = ''
# Import label encoder 
from sklearn import preprocessing 
  
# label_encoder object knows how to understand word labels. 
label_encoder = preprocessing.LabelEncoder() 
  
# Encode labels in column 'species'. 
df['District_encode'] = label_encoder.fit_transform(df['District']) 
df['District_encode'].unique()

import pickle
df1 = df.drop(df.columns[[0,3,4,5,6,7,8]], axis = 1)
X = df1.drop('june',axis=1)
Y = df1['june']

june = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
june.fit(X, Y)
pickle.dump(june, open('HR_Rice/june.pkl', 'wb'))



df2 = df.drop(df.columns[[0,2,4,5,6,7,8]], axis = 1)
X = df2.drop('july',axis=1)
Y = df2['july']

july = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
july.fit(X,Y)
pickle.dump(july, open('HR_Rice/july.pkl', 'wb'))



df3 = df.drop(df.columns[[0,2,3,5,6,7,8]], axis = 1)
X = df3.drop('august',axis=1)
Y = df3['august']

august = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
august.fit(X, Y)
pickle.dump(august, open('HR_Rice/august.pkl', 'wb'))



df4 = df.drop(df.columns[[0,2,3,4,6,7,8]], axis = 1)
X = df4.drop('september',axis=1)
Y = df4['september']

september = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
september.fit(X, Y)
pickle.dump(september, open('HR_Rice/september.pkl', 'wb'))



df5 = df.drop(df.columns[[0,2,3,4,5,7,8]], axis = 1)
X = df5.drop('october',axis=1)
Y = df5['october']

october = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
october.fit(X, Y)
pickle.dump(october, open('HR_Rice/october.pkl', 'wb'))



df6 = df.drop(df.columns[[0,2,3,4,5,6,8]], axis = 1)
X = df6.drop('november',axis=1)
Y = df6['november']

november = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
november.fit(X, Y)
pickle.dump(november, open('HR_Rice/november.pkl', 'wb'))



X = df.drop(['Year','District', 'District_encode'],axis=1)
train_dataset = X.sample(frac=0.8,random_state=0)
test_dataset = X.drop(train_dataset.index)

train_labels = train_dataset.pop('Yield')
test_labels = test_dataset.pop('Yield')

def build_model():
  model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

model = build_model()

EPOCHS = 1000

history = model.fit(
  train_dataset, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[tfdocs.modeling.EpochDots()])

model = build_model()

# The patience parameter is the amount of epochs to check for improvement
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

early_history = model.fit(train_dataset, train_labels, 
                    epochs=EPOCHS, validation_split = 0.2, verbose=0, 
                    callbacks=[early_stop, tfdocs.modeling.EpochDots()])

loss, mae, mse = model.evaluate(test_dataset, test_labels, verbose=2)

print("Testing set Mean Abs Error: {:5.2f} Yield".format(mae))

model.save('HR_Rice')


