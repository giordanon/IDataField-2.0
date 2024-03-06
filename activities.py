import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_multipage import MultiPage
import numpy as np
import os as os
import functions as fx
import datetime

def app():    
    
    uploaded_file = st.file_uploader("Upload LABELS_INPUT", type=["csv", "xlsx"])
    
    if uploaded_file:
        data = pd.read_excel(uploaded_file, sheet_name = "LABELS_INPUT")
        dfa = pd.read_excel(uploaded_file, sheet_name = "Activities")
        pheno = pd.read_excel(uploaded_file, sheet_name = "Phenology")
        
    if uploaded_file:
        data = fx.explode_labels(data)
        ACTIVITY = st.selectbox('ACTIVITY', dfa['Activity name'].unique()) 
        DATE = st.date_input("When was the activity done?", value=None)
        
        STAGE = st.selectbox('Crop stage? Check right crop stage [here](https://bookstore.ksre.ksu.edu/pubs/MF3300.pdf)',
                             pheno['GS'].unique())  
        LOCATION = st.multiselect('LOCATION', data['LOC_SHORT'].unique())
        TRIAL = st.multiselect('TRIAL', data['TRIAL_SHORT'].unique())
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
        
        