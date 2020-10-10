
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error 
import tensorflow as tf
from tensorflow.keras.models import load_model


from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle

# %matplotlib inline

path = r"C:\Users\anush\OneDrive\Desktop\SIH-Project-Central-Crew\Utils\Final processed csv files\UP_Wheat.csv"
df = pd.read_csv(path)

df['District_encode'] = ''
# Import label encoder
from sklearn import preprocessing

# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()

# Encode labels in column 'species'.
df['District_encode'] = label_encoder.fit_transform(df['District'])
df['District_encode'].unique()

df1 = df.drop(df.columns[[0, 3, 4, 5, 6, 7]], axis=1)
X = df1.drop('october', axis=1)
Y = df1['october']
october = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
october.fit(X, Y)
pickle.dump(october, open('UP_Wheat/october.pkl', 'wb'))

# input = [[2020, 0]]
# output = october.predict(input)

df2 = df.drop(df.columns[[0, 2, 4, 5, 6, 7]], axis=1)
X = df2.drop('november', axis=1)
Y = df2['november']
november = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
november.fit(X, Y)
pickle.dump(november, open('UP_Wheat/november.pkl', 'wb'))



# input = [[2020, 0]]
# output = november.predict(input)

df3 = df.drop(df.columns[[0, 2, 3, 5, 6, 7]], axis=1)
X = df3.drop('december', axis=1)
Y = df3['december']
december = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
december.fit(X, Y)
pickle.dump(december, open('UP_Wheat/december.pkl', 'wb'))

# input = [[2020, 0]]
# output = december.predict(input)

df4 = df.drop(df.columns[[0, 2, 3, 4, 6, 7]], axis=1)
X = df4.drop('january', axis=1)
Y = df4['january']
january = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
january.fit(X, Y)
pickle.dump(january, open('UP_Wheat/january.pkl', 'wb'))

# input = [[2020, 0]]
# output = january.predict(input)

df5 = df.drop(df.columns[[0, 2, 3, 4, 5, 7]], axis=1)
X = df5.drop('february', axis=1)
Y = df5['february']
february = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
february.fit(X, Y)
pickle.dump(february, open('UP_Wheat/february.pkl', 'wb'))

# input = [[2020, 0]]
# output = february.predict(input)

X = df.drop(['Year', 'District', 'District_encode'], axis=1)
train_dataset = X.sample(frac=0.8, random_state=0)
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
    epochs=EPOCHS, validation_split=0.2, verbose=0,
    callbacks=[tfdocs.modeling.EpochDots()])

model = build_model()

# The patience parameter is the amount of epochs to check for improvement
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

early_history = model.fit(train_dataset, train_labels,
                          epochs=EPOCHS, validation_split=0.2, verbose=0,
                          callbacks=[early_stop, tfdocs.modeling.EpochDots()])

loss, mae, mse = model.evaluate(test_dataset, test_labels, verbose=2)

print("Testing set Mean Abs Error: {:5.2f} Yield".format(mae))



model.save('UP_Wheat')
























