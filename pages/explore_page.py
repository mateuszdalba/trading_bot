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
            #start_date = st.date_input(label='start date',value=datetime.date(2022, 5, 2))
            #end_date = st.date_input(label='end date',value=datetime.date(2022, 5, 4 ))
            #data = binance_api_data(asset=name ,start=str(start_date),end=str(end_date), timeframe="1m")
            fetch = st.button(label='Start Bot')
            stop_btn = st.button('Stop Bot')
            clear_btn = st.button('Clear Dataframe')

        if clear_btn:
            df = pd.read_pickle('objects/live_data.pkl')
            df_empty = df[0:0]
            df_empty.to_pickle('objects/live_data.pkl')
            st.success('Dataframe cleared !')

        placeholder = st.empty()
       
        if fetch:
            while not stop_btn:
                #data = binance_api_data(asset=name ,start=str(start_date),end=str(end_date), timeframe="1m")
                #x = pd.DataFrame([])
                #x.to_pickle('objects/live_data.pkl')
                #break

                df = pd.read_pickle('objects/live_data.pkl')

                #key = f"https://api.binance.com/api/v3/ticker/price?symbol={name}"
                key = f'https://fapi.binance.com/fapi/v1/ticker/price?symbol={name}'
                data = requests.get(key)  
                data = data.json()
                #st.write(f"{data['symbol']} price is {data['price']}, time is {pd.to_datetime(data['time'],unit='ms')}")
                    
                df2 = pd.DataFrame([{'Symbol':data['symbol'], 'Price':data['price'],'Date':pd.to_datetime(data['time'],unit='ms')}])

                df_live = pd.concat([df,df2])
                df_live.to_pickle('objects/live_data.pkl')

                #time.sleep(1)

                with placeholder.container():

                    col1, col2 = st.columns([1,3])

                    with col1:
                        col1.subheader(f'Live Dataframe for {name}')
                        st.dataframe(df_live[['Price','Date']].sort_values(by='Date',ascending=False))


                    with col2:
                        col2.subheader(f'Live Chart for {name}')
                        fig = px.line(df_live,x='Date',y='Price', markers=True)
                        st.plotly_chart(fig)

                    try:
                        metric1, metric2, metric3 = st.columns(3)
                        previous_price, current_price = df_live['Price'].iloc[-2],df_live['Price'].iloc[-1]
                        metric1.metric('Current Price', float(current_price), f'{np.round(float(current_price)-float(previous_price),4)}')
                    except:
                        st.write('Not enough datapoints to calculate metrics')




        