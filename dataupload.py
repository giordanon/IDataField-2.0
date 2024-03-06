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
    TRAIT = 'Whole Plant Weight'
    TRAIT_2 = 'Head Weight'
    TRAIT_3= 'Head Number'
    TRAIT_4 = 'Stover Weight'
    
    with col1: 
        MASS = st.number_input('Whole Plant Biomass (g)')
    with col2: 
        MASS_2 = st.number_input(f'{TRAIT_2} (g)')
    with col3:
        MASS_3 = st.number_input(f'{TRAIT_3}')
    with col4:
        MASS_4 = st.number_input(f'{TRAIT_4} (g)')
        
    if st.button('LOAD DATAPOINT'):
        df = fx.upload_partitioning(ID, TRAIT, TRAIT_2, TRAIT_3, TRAIT_4, MASS, MASS_2, MASS_3, MASS_4)
        st.dataframe(df)