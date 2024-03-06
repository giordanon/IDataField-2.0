import activities, dataupload, dataupload_other_data, labels, canopy_c, combinedata, seeds, merge_data, labels_stakes, welcome, field_data_uploader
import streamlit as st
from PIL import Image

PAGES = {  
    'Welcome!' : welcome,
    'Upload Activity': activities,
    'Partitioning Data Uploader': dataupload ,
    'Field Data Uploader': field_data_uploader,
    'Bag Labels Generator': labels, 
    'Stakes Labels Generator': labels_stakes,
    'Lab Data Uploader': dataupload_other_data,
    'Canopy Cover Uploader': canopy_c, 
    'Seed counter': seeds, 
    'Combine Data Uploader': combinedata, 
    'Merge Data': merge_data
}

#st.write(st.__version__) # Line to check streamlit version
st.title('IDataField')
st.sidebar.empty()
logoksuwheat = Image.open('INPUT/logo_ksuwheat.jpg')
st.sidebar.image(logoksuwheat, use_column_width=True)
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()