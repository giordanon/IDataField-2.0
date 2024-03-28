import pandas as pd 
import numpy as np
import os as os
import streamlit as st
import functions as fx

def app():
    st.caption('Before generating the labels for Canopy Cover, check that the trials have all the necessary sample timing.')

    if os.path.isfile('Metadata.xlsx'):
        data = pd.read_excel('Metadata.xlsx')
        labels = fx.explode_cc_labels(data)
        
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            STAGE = st.selectbox('ACTIVITY', labels['SAM'].unique())  
        with col2:
            TRIAL = st.selectbox('Trial', labels['TRIAL_SHORT'].unique())
            TRIAL = [TRIAL] if isinstance(TRIAL, str) else TRIAL    
        with col3: 
            YEAR = st.selectbox('YEAR', labels['YEAR'].unique())
        st.caption('You must select all locations where the trial is planted')
        options = labels[labels['TRIAL_SHORT'].isin(TRIAL)]['LOC_SHORT'].unique()
        default_locations = labels['LOC_SHORT'].unique()
        default_locations = [loc for loc in default_locations if loc in options]  # Filter out default values not in options
        LOCATION = st.multiselect('LOCATION', options, default=default_locations)
    
        idx = labels['SAM'].isin([STAGE]) & labels['LOC_SHORT'].isin(LOCATION) & labels['TRIAL_SHORT'].isin(TRIAL) & labels['YEAR'].isin([YEAR])
        data = labels[idx]
        
        
    
    #if st.button('Image Cut'):
    st.session_state["button_pressed"] = True

    if st.session_state.get("button_pressed", False):
        TRIAL = ''.join(str(i) for i in data['TRIAL_SHORT'].unique())
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/01-Canopy Cover/{TRIAL}/'
        filename = f'{out_filepath}/{TRIAL}_cc.csv'
        
        if not os.path.exists(out_filepath):
            os.makedirs(out_filepath)
            
        if os.path.isfile(filename):
            data = pd.read_csv(filename)  
            
        if not os.path.isfile(filename):
            data['Pixels To Crop'] = None
            data['Rotation'] = 0
        st.subheader("Define the pixels to cut")    
        query = st.selectbox("Filter de location to edit", data['LOC_SHORT'].unique())  
        mask = data['LOC_SHORT'].isin([query])
        data = data[mask]
        
        with st.form("data_editor_form"):
            st.caption("Specify the number of pixels to cut")
            edited = st.data_editor(data, 
                                   use_container_width=True,
                                   num_rows="fixed",
                                   hide_index=True,
                                   disabled=["YEAR", "TRIAL_SHORT", "LOC_SHORT", "Plot", "LABEL", "SAM"],
                                   column_order = ("TRIAL_SHORT", "LOC_SHORT", "YEAR", "Plot", "LABEL", "Rotation","Pixels To Cut"),
                                   column_config = {"Pixels To Cut": st.column_config.NumberColumn(format="%f", min_value = 0, max_value=5500)})
            submit_button = st.form_submit_button("Save")
        if submit_button:
            try:
                edited.to_csv(filename, index=False)
                st.dataframe(edited)
                st.success("Table updated")
                time.sleep(5)
            except:
                st.warning("Error updating table")
            st.experimental_rerun()