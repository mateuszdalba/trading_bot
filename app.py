import streamlit as st
from streamlit_option_menu import option_menu

from pages.explore_page import show_explore_page
from pages.predict_page import show_predict_page
 
st.set_page_config(layout="wide")
#page = st.sidebar.selectbox("Choose page", ("Explore","Predict"))

with st.sidebar:
    page = option_menu('Navigate', ["Trading Bot",'Crypto Finder'], 
        icons=['house', 'cloud-upload'], 
        menu_icon="cast", default_index=0,
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    })


if page == "Crypto Finder":
    show_predict_page()
elif page =='Trading Bot':
    show_explore_page()