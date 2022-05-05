# Import libraries
import streamlit as st
import pickle
import numpy as np
import datetime
from functions.API_coingeko import coingeko_api_data
from functions.API_binance import binance_api_data
import time
import datetime
import json
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def show_explore_page():
    
    choose_1 = ('binance','coingeko')

    with st.sidebar:
        api = st.radio(label='Choose API', options=choose_1)

    if api == 'coingeko':

        names = ('bitcoin','ripple',)
        currs = ('eur','usd')
        dayz = [str(i) for i in range(1,366)]

        with st.sidebar:
            name = st.selectbox('Cryptocurrency ID',names)
            curr = st.selectbox('Currency',currs)
            days = st.selectbox('Days',dayz)

        data = coingeko_api_data(name=name,curr=curr ,days=days)

    elif api =='binance':

        names = ('1INCHUSDT','BTCUSDT','ETHUSDT','XRPUSDT','TRXUSDT')
            
        with st.sidebar:
            name = st.selectbox('Cryptocurrency ID',names)
            fetch = st.button(label='Start Bot')
            stop_btn = st.button('Stop Bot')
            clear_btn = st.button('Clear Dataframe')
            set_curr_price = st.button('Set Current Price')
            buy_btn = st.button('Buy')
            if set_curr_price == True:
                f = open('/objects/current_price.txt', 'r')
                curr_price = f.readline()
                f.close()
                buy_price = st.number_input('Buy Price',value=curr_price)
            else:
                buy_price = st.number_input('Buy Price')

        if clear_btn:
            df = pd.read_pickle('objects/live_data.pkl')
            df_empty = df[0:0]
            df_empty.to_pickle('objects/live_data.pkl')
            st.success('Dataframe cleared !')

        placeholder = st.empty()
        
        if fetch:
            while not stop_btn:
                
                df = pd.read_pickle('objects/live_data.pkl')
              
                #key = f"https://api.binance.com/api/v3/ticker/price?symbol={name}"
                key = f'https://fapi.binance.com/fapi/v1/ticker/price?symbol={name}'
                data = requests.get(key)  
                data = data.json()
                df2 = pd.DataFrame([{'Symbol':data['symbol'], 'Price':data['price'],'Date':data['time']}])
                df2=df2.set_index("Date",drop=False)
                df2.index=pd.to_datetime(df2.index,unit="ms")
                df2['Date'] = pd.to_datetime(df2['Date'],unit='ms')
                df_live = pd.concat([df,df2])
                df_live = df_live.drop_duplicates()
                
                df_live.to_pickle('objects/live_data.pkl')
                
                #Save current price to text file
                curr_price = float(df_live['Price'].iloc[-1])
                with open('/objects/current_price.txt', 'w') as f:
                    f.write('%d' % curr_price)   

                time.sleep(1)

                if df_live.shape[0] > 5:
                    df_live['MA'] = df_live['Price'].rolling(window=5).mean()
                    df_live['MA'] = np.round(df_live['MA'],4)

                
                with placeholder.container():

                    col1, col2 = st.columns([1,3])

                    with col1:
                        col1.subheader(f'Live Dataframe for {name}')
                        st.dataframe(df_live[['Price','Date']].sort_values(by='Date',ascending=False))

                    with col2:
                        col2.subheader(f'Live Chart for {name}')
                        if df_live.shape[0] > 5:
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(x=df_live['Date'], y=df_live['Price'],mode='lines+markers',name='Price'))
                            fig.add_trace(go.Scatter(x=df_live['Date'], y=df_live['MA'],mode='lines+markers',name='MA'))
                            #fig = px.line(df_live,x='Date',y='Price', markers=True)
                            st.plotly_chart(fig)

                    
                    metric1, metric2, metric3 = st.columns(3)
                    try:
                        previous_price, current_price = df_live['Price'].iloc[-2],df_live['Price'].iloc[-1]
                    except:
                        previous_price, current_price = 0,0 

                    metric1.metric('Current Price', float(current_price), f'{np.round(float(current_price)-float(previous_price),4)}')

                    if buy_btn:
                        metric2.metric(f'You bought {name} for:', float(buy_price))




        