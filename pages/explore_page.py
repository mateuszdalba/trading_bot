import streamlit as st
import pickle
import numpy as np
from API import API


def show_explore_page():
    st.write('Explore Data')
    
    names = (
    'bitcoin',
    'ripple'
    )
    currs = (
        'eur',
        'usd'
        )

    dayz = [str(i) for i in range(1,366)]
    
    name = st.selectbox('Cryptocurrency ID',names)
    curr = st.selectbox('Currency',currs)
    days = st.selectbox('Days',dayz)
    
    
    data_load_state = st.text('Loading data...')
    data = API(name=name,curr=curr ,days=days)
    data_load_state.text('Loading data...done!')
    
    
    st.write(data)