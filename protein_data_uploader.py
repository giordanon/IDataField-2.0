import pandas as pd 
import streamlit as st
import functions as fx
import os

def app():
    if os.path.isfile('metadata/Labels.csv'):
        data = pd.read_csv('metadata/Labels.csv') # Specify the sheet that is reading
        data = fx.explode_labels(data)
    st.title("Upload Grain Protein Concentration")

    upload_data = st.file_uploader('Upload data from NIR', type = ['csv', 'xlsx'])
    if upload_data:
        if upload_data.type == 'csv/text':
            df = pd.read_csv(upload_data)
        else:
            df = pd.read_excel(upload_data)
        st.dataframe(df)
    if 'input_text' not in st.session_state:
        st.session_state.input_text =''
        
    
    ID = st.text_input('Sample ID', value=st.session_state.input_text)
    TRAIT = 'GPC'
    if ID:
        TRIAL, LOCATION, YEAR, SAMPLING, PLOT = ID.split('-')
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/01-Data/{TRIAL}/'
        filename = f'{out_filepath}/{TRIAL}_field.csv'

        if not os.path.exists(out_filepath):
            os.makedirs(out_filepath)
            
        if os.path.isfile(filename):
            temp_trial = pd.read_csv(filename)
            if not TRAIT in temp_trial.columns and TRAIT == 'GPC':
                temp_trial['GPC'] = None
        
        if not os.path.isfile(filename):
            temp_trial = data[(data['YEAR'] == YEAR) & (data['TRIAL_SHORT'] == TRIAL)]
            temp_trial = temp_trial[["YEAR", "LOC_SHORT", "Plot"]].drop_duplicates()
            
            if TRAIT == 'GPC':
                temp_trial['GPC'] = None
        idx = df['Sample ID'] == ID
        idx_df = df[idx]
        if not idx_df.empty:
            Protein = float(idx_df['Protein Fixed=12 %, NIR'].iloc[0])
            temp_trial.loc[ (temp_trial['LOC_SHORT'] == LOCATION) & (temp_trial['Plot'] == int(PLOT)), 'GPC'] = Protein
            #st.dataframe(temp_trial)
            temp_trial.to_csv(filename, index = False)
            st.success(f':white_check_mark: Protein: {Protein} for {ID} was saved :white_check_mark:')
            st.session_state.input_text = ''
        else:
            st.error(':warning: Sample ID not found :warning:')