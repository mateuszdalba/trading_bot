import time
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import urllib.request, json
import os
import numpy as np
from binance.client import Client
import tensorflow as tf
from tensorflow import keras

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score 
from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance, accuracy_score
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import LSTM 
from itertools import cycle

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots



def live_prediction(asset='BTCUSDT',start="2022.03.17", end="2022.03.18", timeframe="1m"):

    api_key = os.environ.get('api1')
    secret_key = os.environ.get('secret1')

    client = Client(api_key=api_key, api_secret=secret_key)
    scaler_X = MinMaxScaler(feature_range=(0,1))
    scaler_y = MinMaxScaler(feature_range=(0,1))
    
    hist = []
    target = []
    length = 90
    
    try:
        df= pd.DataFrame(client.get_historical_klines(asset, timeframe,start,end))
        df=df.iloc[:,:6]
        df.columns=["Date","Open","High","Low","Close","Volume"]
        df=df.set_index("Date")
        df.index=pd.to_datetime(df.index,unit="ms")
        df=df.astype("float")
        #print(df)
        
    except:
        client = Client(api_key=api_key, api_secret=secret_key)
        
        df= pd.DataFrame(client.get_historical_klines(asset, timeframe,start,end))
        df=df.iloc[:,:6]
        df.columns=["Date","Open","High","Low","Close","Volume"]
        df=df.set_index("Date")
        df.index=pd.to_datetime(df.index,unit="ms")
        df=df.astype("float")
        #print(df)

    #Modeling
    df_mdl = df[['Open','High','Low','Volume','Close']]

    return df_mdl