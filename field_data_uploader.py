import pandas as pd 
import numpy as np
import os as os
import streamlit as st
import functions as fx

def app():
    if os.path.isfile('metadata/Labels.csv'):
        data = pd.read_csv('metadata/Labels.csv') # Specify the sheet that is reading
        data = fx.explode_labels(data)
        # Read Traits
        #traits = pd.read_csv('metadata/Traits.csv') 
    
    #st.dataframe(data)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        YEAR = st.selectbox('Season (harvest year)', data['YEAR'].unique())
    with col2:
        options = data[data['YEAR'].isin([YEAR])]['TRIAL_SHORT'].unique()
        TRIAL = st.selectbox('Trial', options)
    with col3:
        options = data[data['TRIAL_SHORT'].isin([TRIAL]) & data['YEAR'].isin([YEAR])]['SAMPLING'].unique()
        TRAIT = st.selectbox('Trait', options)
    
    if st.button('Lauch field data uploader'):
            st.session_state["button_pressed"] = True

    if st.session_state.get("button_pressed", False):

        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/01-Data/{TRIAL}/'
        filename = f'{out_filepath}/{TRIAL}_field.csv'

        if not os.path.exists(out_filepath):
            os.makedirs(out_filepath)
            
        if os.path.isfile(filename):
            temp_trial = pd.read_csv(filename)
            
            if not TRAIT in temp_trial.columns and TRAIT == 'FHS':
                for i in range(1, 11):
                    temp_trial[f'FHS{i}'] = None
                    
            if not TRAIT in temp_trial.columns and TRAIT == 'PH':
                for i in range(1, 11):
                    temp_trial[f'PH{i}'] = None
                    
            if not TRAIT in temp_trial.columns:
                temp_trial[TRAIT] = None
                
        if not os.path.isfile(filename):
            temp_trial = data[(data['YEAR'] == YEAR) & (data['TRIAL_SHORT'] == TRIAL)]
            temp_trial = temp_trial[["YEAR", "LOC_SHORT", "Plot"]].drop_duplicates()
            
            if TRAIT == 'FHS':
                for i in range(1, 11):
                    temp_trial[f'FHS{i}'] = None
                    
            if TRAIT == 'PH':
                for i in range(1, 11):
                    temp_trial[f'PH{i}'] = None
            if TRAIT != 'PH':  
                temp_trial[TRAIT] = None
            if TRAIT != 'FHS':  
                temp_trial[TRAIT] = None
            if 'FHS' in temp_trial.columns:
                del temp_trial['FHS']
            if 'PH' in temp_trial.columns:
                del temp_trial['PH']
                
            temp_trial.to_csv(filename, index = False)
            
            
        # edit the dataframe 
        with st.form("data_editor_form"):
            st.caption("Load data below")
            edited = st.data_editor(temp_trial, 
                                    use_container_width=True, 
                                    num_rows = "fixed", 
                                    hide_index=True,
                                    disabled = ("YEAR", "LOC_SHORT", "Plot"), 
                                    column_config = {str(TRAIT): st.column_config.NumberColumn(format = "%f") })
            submit_button = st.form_submit_button("Submit")   

        if submit_button:
            try:
                edited.to_csv(filename, index = False)
                st.dataframe(edited)
                st.success("Table updated")
                time.sleep(5)
            except:
                st.warning("Error updating table")
            st.experimental_rerun()

        
                
   
