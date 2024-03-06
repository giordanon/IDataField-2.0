import pandas as pd 
import numpy as np
import os as os
import streamlit as st
import functions as fx

def app():
    st.title('Field Data Uploader')

    data = pd.read_excel('Metadata.xlsx')
    data = fx.explode_labels(data)
    
    #st.dataframe(data)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        YEAR = st.selectbox('Season (harvest year)', data['YEAR'].unique())
    with col2:
        TRIAL = st.selectbox('Trial', data['TRIAL_SHORT'].unique())
    with col3:
        TRAIT = st.selectbox('Trait', ['GPC', 'STAND_COUNT', 'TILLER_COUNT', 'PLANT_HEIGHT', 'FHS'])
    
    if st.button('Lauch field data uploader'):
            st.session_state["button_pressed"] = True

    if st.session_state.get("button_pressed", False):

        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/01-Data/{TRIAL}/'
        filename = f'{out_filepath}/{TRIAL}_{TRAIT}.csv'

        if not os.path.exists(out_filepath):
            os.makedirs(out_filepath)
            
        if os.path.isfile(filename):
            temp_trial = pd.read_csv(filename)
                
        if not os.path.isfile(filename):
            temp_trial = data[(data['YEAR'] == YEAR) & (data['TRIAL_SHORT'] == TRIAL)]
            temp_trial = temp_trial[["YEAR", "LOC_SHORT", "Plot"]].drop_duplicates()
            temp_trial[TRAIT] = np.nan
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

        
                
   
