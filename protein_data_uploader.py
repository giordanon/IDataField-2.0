import pandas as pd 
import streamlit as st
import functions as fx
import os

def app():
    if os.path.isfile('metadata/Labels.csv'):
        data = pd.read_csv('metadata/Labels.csv') # Specify the sheet that is reading
        data = fx.explode_labels(data)
    st.title("Upload Grain Protein Concentration")

    upload_data = st.file_uploader('Upluad data from NIR', type = ['csv', 'xlsx'])
    if upload_data:
        if upload_data.type == 'csv/text':
            df = pd.read_csv(upload_data)
        else:
            df = pd.read_excel(upload_data)
        st.dataframe(df)
    if 'input_text' not in st.session_state:
        st.session_state.input_text =''
        
    
    ID = st.text_input('Sample ID', value=st.session_state.input_text)
    GPC = 'GPC'
    Protein_12 = 'P12'
    Hardness = 'HAR'
    Grain_Moisture = 'GPM'
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
            
            if not GPC in temp_trial.columns:
                temp_trial['GPC'] = None
            if not Grain_Moisture in temp_trial.columns:
                temp_trial['GPM'] = None    
            if not Protein_12 in temp_trial.columns:
                temp_trial['P12'] = None 
            if not Hardness in temp_trial.columns:
                temp_trial['HAR'] = None
        
        if not os.path.isfile(filename):
            temp_trial = data[(data['YEAR'] == YEAR) & (data['TRIAL_SHORT'] == TRIAL)]
            temp_trial = temp_trial[["YEAR", "LOC_SHORT", "Plot"]].drop_duplicates()
            
            temp_trial['GPC'] = None
            temp_trial['GPM'] = None
            temp_trial['P12'] = None
            temp_trial['HAR'] = None
            
        idx = df['Sample ID'] == ID
        idx_df = df[idx]
        if not idx_df.empty:
            
            gpc = float(idx_df['Protein Dry basis %, NIR'].iloc[0])
            temp_trial.loc[ (temp_trial['LOC_SHORT'] == LOCATION) & (temp_trial['Plot'] == int(PLOT)), 'GPC'] = gpc
            
            grain_moisture = float(idx_df['Moisture %, NIR'].iloc[0])
            temp_trial.loc[ (temp_trial['LOC_SHORT'] == LOCATION) & (temp_trial['Plot'] == int(PLOT)), 'GPM'] = grain_moisture
            
            Protein_12 = float(idx_df['Protein Fixed=12 %, NIR'].iloc[0])
            temp_trial.loc[ (temp_trial['LOC_SHORT'] == LOCATION) & (temp_trial['Plot'] == int(PLOT)), 'P12'] = Protein_12
            
            hardness = float(idx_df['Hardness As is %, NIR'].iloc[0])
            temp_trial.loc[ (temp_trial['LOC_SHORT'] == LOCATION) & (temp_trial['Plot'] == int(PLOT)), 'HAR'] = hardness
  
            temp_trial.to_csv(filename, index = False)
            
            st.success(f':white_check_mark: Sample {ID} was saved :white_check_mark:')
            st.success(f' Protein: {gpc}, Moisture: {grain_moisture}, Protein 12 %: {Protein_12}, Hardness: {hardness}')

            st.session_state.input_text = ''
        else:
            st.error(':warning: Sample ID not found :warning:')