import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_multipage import MultiPage
import numpy as np
import os as os
import functions as fx
import datetime

def app():    
    
    metadata = 'Metadata.xlsx'
    data = pd.read_excel(metadata, sheet_name = "LABELS_INPUT")
    dfa = pd.read_excel(metadata, sheet_name = "Activities")
    pheno = pd.read_excel(metadata, sheet_name = "Phenology")
    data = fx.explode_labels(data)
    #st.dataframe(data)
    os.remove('labels.csv')
    ACTIVITY = st.selectbox('ACTIVITY', dfa['Activity name'].unique()) 
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        DATE = st.date_input("Date of activity", value=None)
    with col2:
        STAGE = st.selectbox('Crop stage? [Ref](https://bookstore.ksre.ksu.edu/pubs/MF3300.pdf)',
                         pheno['GS'].unique())  
    with col3: 
        LOCATION = st.multiselect('LOCATION', data['LOC_SHORT'].unique())
    with col4:
        TRIAL = st.multiselect('TRIAL', data['TRIAL_SHORT'].unique())
    with col5:
        YEAR = st.selectbox('YEAR', data['YEAR'].unique())
        
    COMMENTS = st.text_input('Is there anything we should know about the activity?')
            
    if YEAR:  
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/02-Labels/'
        
    st.write("In the comments section you can tell us if something went wrong. Your comments are very valueable to identify problematic plots.")
    
    if st.button('SAVE ACTIVITY'):
        
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        folder_path = f'../{year_folder}/03-Activities'
        
        filename = f'{folder_path}/Activities_Dates.csv'
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        if not os.path.isfile(f'{filename}'): 
            df_create = pd.DataFrame(columns = ['LOCATION', 'YEAR', 'TRIAL', 'STAGE', 'ACTIVITY','DATE', 'COMMENTS'])
            df_create.to_csv(filename, index = False)
            
        df = pd.read_csv(filename)
        values_to_add = {'LOCATION':[LOCATION], 'YEAR':YEAR,'TRIAL':[TRIAL], 'STAGE':STAGE,'ACTIVITY':ACTIVITY,'DATE': DATE, 'COMMENTS':COMMENTS}
        temp1 = pd.DataFrame(values_to_add)
        temp1 = temp1.explode('LOCATION').explode('TRIAL')
        
        df = pd.concat([df, temp1])
        df.to_csv(filename, index = False)
        
        