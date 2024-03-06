import pandas as pd 
import numpy as np
import os as os
import streamlit as st
import functions as fx

def app():
    st.title('Labels Generator App')
       
    df1 = pd.DataFrame()
    TIME = None
    
    uploaded_file = st.file_uploader("Upload LABELS_INPUT", type=["csv", "xlsx"])
    if uploaded_file:
        data = pd.read_excel(uploaded_file)
        pheno = pd.read_excel(uploaded_file, sheet_name = "Phenology") # PHENOLOGY DATA
        st.dataframe(data)

    if uploaded_file:
        YEAR = st.multiselect('SEASON', data['YEAR'].unique())   
        
    if YEAR: 
        YEAR = YEAR[0]    
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/02-Labels/'
        
    if not os.path.exists(out_filepath):
        os.makedirs(out_filepath)
    
    if st.button('GENERATE BAG LABELS'):  
        df = fx.explode_labels(data)        
        st.dataframe(df)   
        
    labels = pd.read_csv('labels.csv')
    STAGE = st.selectbox('Crop stage? Check right crop stage [here](https://bookstore.ksre.ksu.edu/pubs/MF3300.pdf)',
                             pheno['GS'].unique())  
    
    LOCATION = st.multiselect('LOCATION', labels['LOC_SHORT'].unique())
    TRIAL = st.multiselect('TRIAL', labels['TRIAL_SHORT'].unique())
    YEAR = st.multiselect('YEAR', labels['YEAR'].unique())
    
    SIZE = st.multiselect('Size to Print', ['BIG', 'SMALL'])
    FILENAME = st.text_input('FILE NAME')
    
    idx = labels['SAMPLING'].isin(TIME) & labels['LOC_SHORT'].isin(LOCATION) & labels['TRIAL_SHORT'].isin(TRIAL) & labels['YEAR'].isin(YEAR)
    data = labels[idx]    
    
    if st.button('FILTER LABELS'):
        st.dataframe(data.iloc[:, 3:])
    
    if st.button('DOWNLOAD BAG LABELS'):
        fx.label_generator(data, SIZE, FILENAME, out_filepath)
        os.remove('labels.csv')
        os.remove(f'{out_filepath}pdf1.pdf')
        
        
                
   
