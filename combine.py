import pandas as pd 
import re
import numpy as np
import os as os
import streamlit as st
import functions as fx

def app():

    if os.path.isfile('metadata/Labels.csv'):
        data = pd.read_csv('metadata/Labels.csv') # Specify the sheet that is reading
        labels = fx.explode_labels(data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1: 
            YEAR = st.selectbox('YEAR', labels['YEAR'].unique())
        with col1:
            options = labels[labels['YEAR'].isin([YEAR])]['LOC_SHORT'].unique()
            LOCATION = st.selectbox('LOCATION', options)
        with col2: 
            LENGTH = st.number_input('Insert default plot length in meters for a given field', value = 8.50, step = 0.01)
        with col3: 
            NROW = st.number_input('Insert default number of rows in the planter. Default set to 7.', value = 7.0, step = 1.0)
        with col4: 
            STD_MOIST = st.number_input('Standard grain trading moisture, default to 13.5%', value = 13.5, step = 0.01)
    
        idx =  labels['LOC_SHORT'].isin([LOCATION])  & labels['YEAR'].isin([YEAR])
        data = labels[idx].drop_duplicates(subset=['LABEL'])  
        # Select unique plots for each trial
        data = data.filter(regex = 'YEAR|LOC_SHORT|TRIAL_SHORT|Plot').drop_duplicates()
        data.columns = ['YEAR','TRIAL','LOCATION', 'PLOT']
        
        # Retrieve trials within location
        TRIALS = data['TRIAL'].unique().tolist()
        
        st.dataframe(data)
    
    # Upload combine data
    upload = st.file_uploader("Upload combine data - One field at a time", type=["csv"])
    # Upload Treatments
    treatments =  st.file_uploader("Upload treatments data. Make sure location names and trial names match our keys", type=["csv", "xlsx"])
    
    # edit the dataframe 
    #selection = st.selectbox(f'Do you need to adjust plot length at {LOCATION}', ['Yes', 'No'],index=None )
    
    
    
    if upload and treatments:
        
            treatments = pd.read_excel(treatments)
            treatments.columns = ['LOCATION','TRIAL','TRT1', 'TRT2', 'TRT3', 'PLOT']

            combine = pd.read_csv(upload)
            # Select relevant columns           
            combine = combine.filter(regex = 'RANGE|ROW|TRIAL|PLOT|Weight|Moisture|Test Weight')
            # Rename columns
            combine.columns = ['RANGE', 'ROW', 'TRIAL', 'PLOT', 'Weight', 'Moisture', 'Test Weight']

            # filter out fills and tbds
            # might eb able to remvoe these two
            idx = combine['TRIAL'].isin(TRIALS)
            combine = combine[idx]
            
    #if selection:
     
        #if selection == 'Yes':
    if st.button('Do you want to modify plot length?'):
        st.session_state["button_pressed"] = True

    if st.session_state.get("button_pressed", False):
        with st.form("data_editor_form"):

            st.caption("Modify plot length based on orthophoto.")

            combine['PLOT_LENGTH'] = LENGTH
            combine['ROWS'] = NROW

            edited = st.data_editor(combine, 
                                    use_container_width=True, 
                                    num_rows = "fixed", 
                                    hide_index=True,
                                    disabled = ('RANGE', 'ROW', 'TRIAL', 'PLOT', 'Weight', 'Moisture', 'Test Weight')
                                   )
            submit_button = st.form_submit_button("Submit")

        if submit_button:
            combine = edited
    else:
        st.write(f'No adjustments selected for plot length. Using default plot legth {LENGTH} meters for all plots.')

            
    if st.button('Create yield files'):
        
        for trial in TRIALS:
            # Trial data
            m1 = data[data['TRIAL'] == trial]
            m1['PLOT'] = m1['PLOT'].astype(np.int32)
            # Combine data
            m2 = combine[combine['TRIAL'] == trial]
            m2['PLOT'] = m2['PLOT'].astype(np.int32)
            # Treatments data
            m3 = treatments[treatments['TRIAL'].isin([trial]) & treatments['LOCATION'].isin([LOCATION])]
            m3['PLOT'] = m3['PLOT'].astype(np.int32)

            # Merge DataFrames sequentially
            m4 = pd.merge(m1,m3, on=['LOCATION','TRIAL', 'PLOT'], how = 'left')
            m5 = pd.merge(m4,m2, on=['TRIAL', 'PLOT'], how = 'left')

            m5['AREA'] = m5['PLOT_LENGTH'].astype(np.float64) * m5['ROWS'].astype(np.float64)/np.float64(NROW)  * 0.3048 * np.float64(6)

            m5['W13'] = m5['Weight'].astype(np.float64) * (100 - m5['Moisture'].astype(np.float64) ) /(100 - STD_MOIST)
            m5['W0'] = m5['W13'] * (1 - STD_MOIST/100)


            m5['Yield Std Moist (kg/ha)'] = (m5['W13'] ) / m5['AREA'] * 10000
            m5['Yield Dry Basis (kg/ha)'] = (m5['W0']) / m5['AREA'] * 10000

            m5['Yield Std Moist (bu/ac)'] = ((m5['W13']) / m5['AREA']) * .0149 * 10000
            m5['Yield Dry Basis (bu/ac)'] = ((m5['W0']) / m5['AREA']) *  .0149 * 10000

            m5["TW (kg/hL)"] = m5["Test Weight"]

            m5 = m5[['YEAR','LOCATION','TRIAL', 'RANGE', 'ROW', 'PLOT', "TRT1", "TRT2", "TRT3", "Yield Std Moist (kg/ha)", 
                     "Yield Dry Basis (kg/ha)", "Yield Std Moist (bu/ac)", "Yield Dry Basis (bu/ac)", "TW (kg/hL)", 'Moisture']]

            filename = fx.directory_check_combine(YEAR, trial)

            fx.file_check_combine(LOCATION, filename, m5)




            if m1.shape[0] == m5.shape[0]:
                st.write(f'Success! All observations for trial {trial} saved correctly. Number of observations match. Yield observations of {trial} in {LOCATION} are  {m5.shape[0]}.')
            else:
                st.write(f'Check {trial} in {LOCATION} bacause observations do not match. Yield observations of {trial} in {LOCATION} are  {m5.shape[0]}, you should have {m1.shape[0]} plots according to labels file. ')
                
                
            
            
                    
            
        
    
   
            
            