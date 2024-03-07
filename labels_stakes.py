#Import Libraries
import pandas as pd 
import numpy as np
#Directories management 
import os as os
import streamlit as st
import functions as fx

def app():
    st.title('Stakes Labels Generator App')
    metadata = 'Metadata.xlsx'
    data = pd.read_excel(metadata)   
    df = fx.explode_plot_labels(data)
    #st.dataframe(df)
    df.to_csv("labels.csv", index = False)    

    if os.path.isfile('labels.csv'): 
        labels = pd.read_csv('labels.csv')
        os.remove('labels.csv')

        col1, col2, col3 = st.columns(3)

        with col1:
            TRIAL = st.multiselect('Trial', labels['TRIAL_SHORT'].unique())
        with col2:
            YEAR = st.multiselect('Year', labels['YEAR'].unique())
        with col3:
            FILENAME = st.text_input('File name')

        idx = labels['TRIAL_SHORT'].isin(TRIAL) & labels['YEAR'].isin(YEAR)
        #idx = labels['LOC_SHORT'].isin(LOCATION) & labels['YEAR'].isin(YEAR)
        data = labels[idx]
        
        
        
    if st.button('FILTER LABELS'):
        if YEAR: 
            YEAR = YEAR[0]    
            prev_year = 2000 + int(YEAR) - 1
            year_folder = f'SEASON {prev_year}-{YEAR}'
            out_filepath = f'../{year_folder}/02-Labels/'

        if not os.path.exists(out_filepath):
            os.makedirs(out_filepath)
            
        st.dataframe(data, 
                     hide_index = True, 
                     column_order=("TRIAL_SHORT", "LOC_SHORT","YEAR","SAMPLING","Plot", "LABEL" )
                    )            
    
    uploadedTreatments = st.file_uploader("For PLOT LABELS upload treatments file", type=["csv", "xlsx"])
    # Check if file was uploaded
    if uploadedTreatments:
        if uploadedTreatments.type == "text/csv":
            dataTrt = pd.read_csv(uploadedTreatments)
        else:
            dataTrt = pd.read_excel(uploadedTreatments)
        ## Rename treatments file
        dataTrt.columns = ['LOC_SHORT', 'TRIAL_SHORT', 'TRT1', 'TRT2', 'TRT3', 'Plot']
        st.dataframe(dataTrt.head())
    
    if st.button('DOWNLOAD PLOT LABELS'):
        data = data[['Plot', 'TRIAL_SHORT', 'LOC_SHORT', 'YEAR']]
        
        # Merge data with treatments data
        outPs = data.merge(dataTrt, on=["Plot","TRIAL_SHORT", "LOC_SHORT"])
        
        outPs = outPs.transpose()
        outPs.to_excel(f"{out_filepath}{FILENAME}.xlsx", index=False)
        st.dataframe(outPs)
    
    
