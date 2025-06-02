import functions as fx
import streamlit as st
from PIL import Image
import os
import pandas as pd

def app():
   
    ID = st.text_input('SCAN QR CODE IN LABEL')
    
    if ID: 
        filename, TRIAL, SITE, YEAR, SAMPLING, PLOT = fx.directory_check(ID)
        
        if os.path.exists(filename):
            
            temp_df = pd.read_csv(filename)

            idx =  (temp_df['SITE'] == SITE) & (temp_df['YEAR'] == int(YEAR)) & (temp_df['TRAIT'] == 'TKW') & (temp_df['PLOT'] == int(PLOT))
            temp_df2 = temp_df[idx]

            if temp_df2.shape[0] > 0:
                st.warning(f'TKW for {ID} is already on file. If you continue processing the sample, it will generate a duplicate.', icon="⚠️")
    
    GRAIN_WEIGHT = st.number_input('Mass of the grains sample (g)')
    image = st.file_uploader("Upload Grains Picture")

    if image:
        st.image(image)
        TKW = fx.count_seeds(image, GRAIN_WEIGHT)
              
    if st.button('Check Grains Arrangement'):   
        with Image.open('tempImage.jpg') as image:
            st.image(image)
        os.remove('tempImage.jpg')
        
    if st.button('LOAD TKW DATAPOINT'):
        
        df = fx.upload_partitioning(ID, ["TKW"], [TKW])
        st.dataframe(df.tail(10))
     