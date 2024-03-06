import activities, dataupload, dataupload_other_data, labels, canopy_c, combinedata, seeds, merge_data, labels_stakes, welcome
import streamlit as st
from PIL import Image

PAGES = {  
    'Welcome!' : welcome,
    'Upload Activity': activities,
    'Partitioning Data Uploader': dataupload ,
    'Bag Labels Generator': labels, 
    'Stakes Labels Generator': labels_stakes,
    'Lab Data Uploader': dataupload_other_data,
    'Canopy Cover Uploader': canopy_c, 
    'Seed counter': seeds, 
    'Combine Data Uploader': combinedata, 
    'Merge Data': merge_data
}

st.title('IDataField')
st.sidebar.empty()
logoksuwheat = Image.open('INPUT/logo_ksuwheat.jpg')
st.sidebar.image(logoksuwheat, use_column_width=True)
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()