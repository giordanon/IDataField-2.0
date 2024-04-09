import functions as fx
import streamlit as st
from PIL import Image
import os
import pandas as pd

def app():
   
    ID = st.text_input('SCAN QR CODE IN LABEL')
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
     