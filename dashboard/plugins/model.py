import pickle
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

#load the model
def load_model(file_path):
    with open(file_path, 'rb') as file:
        model = pickle.load(file)

    return model

#predict
def predict(model, df):
    return model.predict(df)

#data preprocessing
def data_preprocessing(df):
    window_size = 60

    #min-max-scaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df)

    # W sequence of past stock prices (X) and the target is the next stock price (y)
    X, y = [], []
    for i in range(window_size, len(df)):
        X.append(df[i-window_size:i, 0])  # Previous 'window_size' prices as the input
        y.append(df[i, 0])  # The next price as the target
    X,y = np.array(X), np.array(y)

    #Reshape X for LSTM (samples, timesteps, features)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    return X,y