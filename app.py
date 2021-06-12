import predict
import analysis
import streamlit as st

PAGES={
    "Predition" : predict,
    "Visualization" : analysis
}


st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()