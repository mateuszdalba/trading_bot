import streamlit as st


from pages.explore_page import show_explore_page
from pages.predict_page import show_predict_page
 

page = st.sidebar.selectbox("Choose page", ("Predict", "Explore"))



if page == "Predict":
    show_predict_page()
else:
    show_explore_page()