import pandas as pd 
import numpy as np
import os as os
import streamlit as st
import functions as fx
from pyproj import CRS
import geopandas as gpd
from geographiclib.geodesic import Geodesic
import simplekml
import functions as fx

def app():
    
    st.caption('To select the Trial, Year, and Location, type CCP in the "Timing" column in the Metadata excel file.')

    if os.path.isfile('Metadata.xlsx'):
        data = pd.read_excel('Metadata.xlsx')
        labels = fx.explode_cc_labels(data)

        col2, col3 = st.columns(2)

        with col2:
            TRIAL = st.selectbox('Trial', labels['TRIAL_SHORT'].unique())
            TRIAL = [TRIAL] if isinstance(TRIAL, str) else TRIAL    
        with col3: 
            YEAR = st.selectbox('YEAR', labels['YEAR'].unique())

        options = labels[(labels['TRIAL_SHORT'].isin(TRIAL)) & (labels['YEAR'] == YEAR)]['LOC_SHORT'].unique()
        LOCATION = st.selectbox('LOCATION', options)

        idx = labels['LOC_SHORT'].isin([LOCATION]) & labels['TRIAL_SHORT'].isin(TRIAL) & labels['YEAR'].isin([YEAR])
        data = labels[idx]

    st.session_state["button_pressed"] = True

    if st.session_state.get("button_pressed", False):
        TRIAL = ''.join(str(i) for i in data['TRIAL_SHORT'].unique())
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/01-Canopy Cover/{LOCATION}/'
        filename = f'{out_filepath}/{TRIAL}.csv'

        if not os.path.exists(out_filepath):
            os.makedirs(out_filepath)

        if os.path.isfile(filename):
            data = pd.read_csv(filename)  

        if not os.path.isfile(filename):
            data['Pixels To Crop'] = None
            data['Rotation'] = 0
            data['Latitude'] = None
            data['Longitude'] = None
        st.subheader("Add Latitude and Longitude in DD")    


        with st.form("data_editor_form"):
            edited = st.data_editor(data, 
                                   use_container_width=True,
                                   num_rows="fixed",
                                   hide_index=True,
                                   disabled=["YEAR", "TRIAL_SHORT", "LOC_SHORT", "Plot", "LABEL", "SAM"],
                                   column_order = ("TRIAL_SHORT", "LOC_SHORT", "YEAR", "Plot", "LABEL", "Latitude", "Longitude"),
                                   column_config = {"Pixels To Cut": st.column_config.NumberColumn(format="%f", min_value = 0, max_value=5500)})
            submit_button = st.form_submit_button("Load Coordinates for kml")
            st.caption("Type the units in meters to move the Latitude, move to the south positive numbers, move to the north negative number ")
            south = st.number_input("Move coordinates (Meters) North(-) South(+):", format= '%f')
           
            west = st.number_input("West", format= '%f')
            
        if submit_button:
            try:
                edited.to_csv(filename, index=False)
                st.dataframe(edited.style.format({'Latitude': "{:.6f}", 'Longitude': "{:.6f}"}))
                st.success("Table updated")
                time.sleep(5)
            except:
                st.warning("Error updating table")
            st.experimental_rerun()
            
    if st.button("Generate kml"):
        df = pd.read_csv(filename)
        df = df[['Plot', 'Latitude', 'Longitude']]
        
        # Adjust coordinates
        adj_c = fx.adjust_coordinates(df, south, west).dropna().reset_index(drop=True)

        # Sort by Latitude and Longitude
        adj_c = adj_c.sort_values(by=['Plot'], ascending=True)

        # Get the last latitude, longitude, and plot number
        last_lat = adj_c.iloc[-1]['Latitude']
        last_long = adj_c.iloc[-1]['Longitude']

        # Plot number for the new row
        new_plot = 999

        # Create a new row with the same latitude, longitude, and incremented plot number
        new_row = pd.DataFrame([[new_plot, last_lat, last_long]], columns=['Plot', 'Latitude', 'Longitude'])

        # Append the new row to the DataFrame
        adj_c = pd.concat([adj_c, new_row], ignore_index=True)
        ilename_kml_csv = f'{out_filepath}/{TRIAL}_kml.csv'
        adj_c.to_csv(ilename_kml_csv, index=True)

        adj_c = gpd.GeoDataFrame(adj_c, geometry=gpd.points_from_xy(adj_c.Longitude, adj_c.Latitude))
        if adj_c.crs is None:
            # Assign CRS for WGS84 (EPSG:4326)
            adj_c.crs = CRS.from_epsg(4326)

        # Ensure geometries are in the assigned CRS
        adj_c = adj_c.to_crs(adj_c.crs)

        # Create a KML object
        kml = simplekml.Kml()

        # Iterate over each row in the GeoDataFrame and add a point to the KML object
        for _, row in adj_c.iterrows():
            kml.newpoint(name=row['Plot'], coords=[(row['Longitude'], row['Latitude'])])
        filename_kml = f'{out_filepath}/{TRIAL}.kml'

        kml.save(filename_kml) 