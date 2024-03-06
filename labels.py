import pandas as pd 
import numpy as np
import os as os
import qrcode, time
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import streamlit as st
import functions as fx

def app():
    st.title('Labels Generator App')
       
    data = pd.read_excel('Metadata.xlsx')
    df = fx.explode_labels(data)        
    #st.dataframe(df)   

    if os.path.isfile('labels.csv'):
        labels = pd.read_csv('labels.csv')
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            STAGE = st.multiselect('Sampling at?', labels['SAMPLING'].unique())  
        with col2:
            LOCATION = st.multiselect('LOCATION', labels['LOC_SHORT'].unique())
        with col3:
            TRIAL = st.multiselect('TRIAL', labels['TRIAL_SHORT'].unique())
        with col4: 
            YEAR = st.multiselect('YEAR', labels['YEAR'].unique())
        with col5:
            SIZE = st.multiselect('Size to Print', ['BIG', 'SMALL'])
    
        idx = labels['SAMPLING'].isin(STAGE) & labels['LOC_SHORT'].isin(LOCATION) & labels['TRIAL_SHORT'].isin(TRIAL) & labels['YEAR'].isin(YEAR)
        data = labels[idx]    
    
    if st.button('FILTER LABELS'):
        st.dataframe(data, 
                     hide_index = True, 
                     column_order=("TRIAL_SHORT", "LOC_SHORT","YEAR","SAMPLING","Plot", "LABEL" )
                    )
        
    FILENAME = st.text_input('Name of the file containing downloaded labels?')
    
    if st.button('DOWNLOAD BAG LABELS'):

        YEAR = YEAR[0]    
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/02-Labels/'

        if not os.path.exists(out_filepath):
            os.makedirs(out_filepath)
        
        fx.label_generator(data, SIZE, FILENAME, out_filepath)
        os.remove('labels.csv')
        os.remove(f'{out_filepath}pdf1.pdf')
        
        
                
   
