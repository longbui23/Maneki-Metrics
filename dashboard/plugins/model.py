import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pickle

#load the model
def load_model(file_path):
    with open(file_path, 'rb') as file:
        model = pickle.load(file)

    return model

#build model
def train_lstm_model(symbol, start_date='2010-01-01', end_date='2024-12-01', window_size=60, epochs=10, batch_size=32):
    # Download historical stock data
    data = yf.download(symbol, start=start_date, end=end_date)

    # Use adjusted close prices for prediction
    data = data[['Adj Close']]

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    #Prepare the data for the LSTM model
    def create_sequences(data, window_size):
        X, y = [], []
        for i in range(window_size, len(data)):
            X.append(data[i-window_size:i, 0])  # Previous 'window_size' prices as the input
            y.append(data[i, 0])  # The next price as the target
        return np.array(X), np.array(y)

    X, y = create_sequences(scaled_data, window_size)

    # Reshape X for LSTM
    X = X.reshape(X.shape[0], X.shape[1], 1)

    #  Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=False, input_shape=(X_train.shape[1], 1)))
    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

    # Train the model
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=1)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Inverse transform the predictions and actual values back to the original scale
    predictions = scaler.inverse_transform(predictions)
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

    return model, predictions, y_test_actual


#predict
def visualize_predictions(symbol, model, data, window_size=60, days_ahead=30):
    data = yf.download(symbol, period="1yr", progress=False)  
    # Get the last `window_size` days from the data for predictions
    recent_data = data['Adj Close'].values[-window_size:]
    scaled_recent_data = scaler.transform(recent_data.reshape(-1, 1))

    predictions = []
    input_sequence = scaled_recent_data.reshape(1, window_size, 1)

    for _ in range(days_ahead):
        next_prediction = model.predict(input_sequence)[0, 0]
        predictions.append(next_prediction)

        # Update the input sequence for the next prediction
        input_sequence = np.append(input_sequence[:, 1:, :], [[[next_prediction]]], axis=1)

    # Inverse transform the predictions
    scaler = MinMaxScaler(feature_range=(0, 1))
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

    # Create a date range for the future predictions
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=days_ahead + 1, freq='B')[1:]

    # Create the plotly figure
    fig = go.Figure()

    # Add predictions to the plot
    fig.add_trace(go.Scatter(x=future_dates, y=predictions, mode='lines', name=f'Next {days_ahead} Days Prediction', line=dict(color='red')))

    # Update the layout
    fig.update_layout(
        title=f'{symbol} Stock Price Prediction',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        template='plotly_dark',
        showlegend=True,
    )

    return fig

