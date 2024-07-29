import activities, dataupload, dataupload_other_data, labels, canopy_c, combinedata, seeds, merge_data, labels_stakes, welcome, field_data_uploader, assgin_coor_to_plots, Image_cut, flight_path_generator, rename_photos, Canopy, Protein, canopy_cover
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

im = Image.open('content/wheat.png')
#st.set_page_config(page_title="IDataField 2.0", page_icon = im)

PAGES = {  
    'Welcome!': welcome,
    'Activities Uploader': activities,
    'Partitioning Data Uploader': dataupload ,
    'Field Data Uploader': field_data_uploader,
    'Lab Data Uploader': dataupload_other_data,
    'Bag Labels Generator': labels, 
    'Stakes Labels Generator': labels_stakes,
    'Assign Plot Coordinates': assgin_coor_to_plots,
    'Canopy Cover Uploader': Canopy, 
    'Seed Counter': seeds, 
    'Combine Data Uploader': combinedata, 
    'Merge Data': merge_data,
    'Protein' : Protein,
    'Canopy Cover' : canopy_cover
    
}
#st.write(st.__version__) # Line to check streamlit version
# Check sync
st.title('IDataField 2.0')
st.sidebar.image(im, use_column_width=True)
with st.sidebar:
    selection = option_menu(menu_title = "Menu", 
                            options = list(PAGES.keys()), 
                            icons = ['house', 'box-arrow-in-down','box-arrow-in-down','box-arrow-in-down','box-arrow-in-down',
                                    'qr-code','qr-code', 'pin-map', 'upc-scan', 'box-arrow-in-down', 'union'], 
                            menu_icon = 'three-dots'
                           )
page = PAGES[selection]
page.app()