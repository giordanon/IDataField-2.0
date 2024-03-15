import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_multipage import MultiPage
import numpy as np
import os as os
import functions as fx


def app():    
    ID = st.text_input('SCAN QR CODE IN LABEL')
    
    col1, col2, col3, col4 = st.columns(4)    
    TRAITS = ['Whole Plant Weight', 'Head Weight','Head Number', 'Stover Weight']
    
    with col1: 
        MASS = st.number_input(f'{TRAITS[0]} (g)')
    with col2: 
        MASS_2 = st.number_input(f'{TRAITS[1]} (g)')
    with col3:
        MASS_3 = st.number_input(f'{TRAITS[2]}')
    with col4:
        MASS_4 = st.number_input(f'{TRAITS[3]} (g)')
        
    WEIGHTS = [MASS, MASS_2, MASS_3, MASS_4]
        
    if st.button('LOAD DATAPOINT'):
        df = fx.upload_partitioning(ID, TRAITS, WEIGHTS)
        st.dataframe(df)