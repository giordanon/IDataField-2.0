#Import Libraries
import pandas as pd 
import numpy as np
#Directories management 
import os as os
# QR code libraries
import qrcode, time
#PDF Libraries
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import streamlit as st

def app():
    st.title('Stakes Labels Generator App')
       
    df1 = pd.DataFrame()
    TIME = None
    # Allow only .csv and .xlsx files to be uploaded
    uploaded_file = st.file_uploader("Upload spreadsheet", type=["csv", "xlsx"])
    # Check if file was uploaded
    if uploaded_file:
        if uploaded_file.type == "text/csv":
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.dataframe(data.head())

    # Create the directory   
    if uploaded_file:
        YEAR = st.multiselect('SEASON', data['YEAR'].unique())   
        
    if YEAR: 
        YEAR = YEAR[0]    
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/02-Labels/'
        
    if not os.path.exists(out_filepath):
        os.makedirs(out_filepath)
    
    if st.button('GENERATE STAKES LABELS'):  

        data = data.dropna().reset_index()
        data['SAMPLING'] = data['SAMPLING'].str.replace(' ', '').str.split(pat = ",",  expand = False)
        data['Trt1'] = pd.Series(dtype = 'object')
        data['Rep1'] = pd.Series(dtype = 'object')
        
        for k,row in data.iterrows():
            data.at[k,'Trt1'] = np.arange(1,int(data.at[k,'Trt'])+1)
            data.at[k,'Rep1'] = np.arange(1,int(data.at[k,'Reps'])+1)
            
        df = data.explode('SAMPLING').explode('Rep1').explode('Trt1')
        df['Plot'] = df['Rep1']*100 + df['Trt1']
        df['LABEL'] = df['TRIAL_SHORT'].astype(str) + '-' + df['LOC_SHORT'].astype(str) + '-' + df['YEAR'].astype(str) + '-' + df['SAMPLING'].astype(str) + '-' + df['Plot'].astype(str)
        df = df.reset_index()        
        st.dataframe(df)

        
        df.to_csv(f"{out_filepath}labels.csv", index = False)    
        
    
      
    labels = pd.read_csv(f'{out_filepath}labels.csv')
    #LOCATION = st.multiselect('LOCATION', labels['LOC_SHORT'].unique())
    TRIAL = st.multiselect('TRIAL', labels['TRIAL_SHORT'].unique())
    YEAR = st.multiselect('YEAR', labels['YEAR'].unique())

    FILENAME = st.text_input('FILE NAME')
    
    idx = labels['TRIAL_SHORT'].isin(TRIAL) & labels['YEAR'].isin(YEAR)
    #idx = labels['LOC_SHORT'].isin(LOCATION) & labels['YEAR'].isin(YEAR)
    data = labels[idx]    
    
    if st.button('FILTER LABELS'):
            st.dataframe(data.iloc[:, 3:])
            
    
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
    
    
