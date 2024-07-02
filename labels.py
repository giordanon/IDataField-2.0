import pandas as pd 
import numpy as np
import os as os
import qrcode, time
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader, PdfFileWriter # Make sure is version 2.0.0
import streamlit as st
import functions as fx

def app():

    if os.path.isfile('metadata/Labels.csv'):
        data = pd.read_csv('metadata/Labels.csv') # Specify the sheet that is reading
        labels = fx.explode_labels(data)
        st.dataframe(labels.iloc[:,2:], use_container_width=True, hide_index=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1: 
            YEAR = st.multiselect('YEAR', labels['YEAR'].unique())
        with col2:
            options = labels[labels['YEAR'].isin(YEAR)]['TRIAL_SHORT'].unique()
            TRIAL = st.multiselect('TRIAL',options)   
        with col3:
            options = labels[labels['TRIAL_SHORT'].isin(TRIAL) & labels['YEAR'].isin(YEAR)]['LOC_SHORT'].unique()
            LOCATION = st.multiselect('LOCATION', options)
        with col4:
            options = labels[labels['LOC_SHORT'].isin(LOCATION) & labels['TRIAL_SHORT'].isin(TRIAL) & labels['YEAR'].isin(YEAR)]['SAMPLING'].unique()
            STAGE = st.multiselect('Sampling at?', options)  
        with col5:
            SIZE = st.multiselect('Size to Print', ['BIG', 'SMALL'])
    
        idx = labels['SAMPLING'].isin(STAGE) & labels['LOC_SHORT'].isin(LOCATION) & labels['TRIAL_SHORT'].isin(TRIAL) & labels['YEAR'].isin(YEAR)
        data = labels[idx].drop_duplicates(subset=['LABEL'])  
    
    if st.button('FILTER LABELS'):
        st.dataframe(data, 
                     hide_index = True, 
                     column_order=("TRIAL_SHORT", "LOC_SHORT","YEAR","SAMPLING","Plot", "LABEL" )
                    )
        
    FILENAME = st.text_input('Name of the file containing downloaded labels?')
    
    if st.button('Generate Bag Labels'):

        YEAR = YEAR[0]    
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/02-Labels/'

        if not os.path.exists(out_filepath):
            os.makedirs(out_filepath)
        
        fx.label_generator(data, SIZE, FILENAME, out_filepath)
        os.remove(f'{out_filepath}pdf1.pdf')
    
        with open(f"{out_filepath}{FILENAME}.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()
    
        if os.path.exists(f"{out_filepath}{FILENAME}.pdf"):
            st.download_button(label="Download Labels",
                                data=PDFbyte,
                                file_name=f"{FILENAME}.pdf",
                                mime='application/octet-stream')
        #os.remove(f'{out_filepath}pdf1.pdf')

        
                
   
