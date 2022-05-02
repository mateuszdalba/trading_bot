import streamlit as st
import pickle
import numpy as np
import datetime
from functions.API_coingeko import coingeko_api_data
from functions.API_binance import binance_api_data


def show_explore_page():

    st.write('Explore Data')
    
    choose_1 = ('binance','coingeko')
    api = st.radio(label='Choose API', options=choose_1)

    data_load_state = st.text('Loading data...')
    if api == 'coingeko':

        names = (
            'bitcoin',
            'ripple',
             )

        currs = (
        'eur',
        'usd'
        )

        dayz = [str(i) for i in range(1,366)]

        name = st.selectbox('Cryptocurrency ID',names)
        curr = st.selectbox('Currency',currs)
        days = st.selectbox('Days',dayz)

        data = coingeko_api_data(name=name,curr=curr ,days=days)
    elif api =='binance':

        names = (
            'BTCUSDT',
            'ETHUSDT'
             )
        name = st.selectbox('Cryptocurrency ID',names)

        start_date = st.date_input(label='start date',value=datetime.date(2022, 3, 17))
        end_date = st.date_input(label='end date',value=datetime.date(2022, 3, 18))


        data = binance_api_data(asset=name ,start=str(start_date),end=str(end_date), timeframe="1m")
        


    data_load_state.text('Loading data...done!')


    
 
    
    
    st.write(data)