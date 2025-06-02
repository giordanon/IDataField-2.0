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
import cv2 as cv
import matplotlib.pyplot as plt

def app():
    tab1, tab2, tab3, tab4, tab5= st.tabs(['Assing Coordinates', 'Flight Path', 'Rename Photos', 'Crop Images', 'Green Canopy Cover'])
    
    with tab1:        
        st.subheader("Upload the field map and the coordinates from the planter")
        col1, col2 = st.columns(2)
        with col1:
            mapPath = st.file_uploader("Upload Field Map", type=['csv', 'xlsx'])
        with col2:
            coordinatesPath = st.file_uploader("Upload Drill Coordinates", type=['csv'])
        if mapPath:
            dfMap = fx.read_map(mapPath)
        if os.path.isfile('metadata/Labels.csv'):
            data = pd.read_csv('metadata/Labels.csv')
            labels = fx.explode_cc_labels(data)
    
            col1, col2 = st.columns(2)
            with col1: 
                YEAR1 = st.selectbox('Year1', labels['YEAR'].unique())
            loc_option1 = labels[(labels['YEAR'] == YEAR1)]['LOC_SHORT'].unique()
            with col2:
                LOCATION = st.selectbox('Location1', loc_option1)
        if coordinatesPath:
            cd = pd.read_csv(coordinatesPath)
            # Drop rows with missing values
            cd = cd[['Name', 'Longitude', 'Latitude']].dropna()
    
            # Extract range number
            # Add one to the number because tractor GPS starts range from zero
            cd['y'] = cd['Name'].str.extract(r'(\d+)').astype(int) + 1
            
            direction = st.selectbox('Planting Direction',
                                   ('South - North', 'West - East', 'North - South', 'East - West'))
    
    
            # Sort coordinates based on direction
            if direction == 'South - North':
                # North
                cd = cd.groupby('y').apply(lambda x: x.sort_values(by='Longitude', ascending=True))
            elif direction =='West - East':
                # East
                cd = cd.groupby('y').apply(lambda x: x.sort_values(by='Latitude', ascending=False))
            elif direction == 'North - South':
                # South
                cd = cd.groupby('y').apply(lambda x: x.sort_values(by='Longitude', ascending=False))
            elif direction == 'East - West':
                # West
                cd = cd.groupby('y').apply(lambda x: x.sort_values(by='Latitude', ascending=True))
            cd.rename(columns={'y': 'temp_y'}, inplace=True)
            cd.reset_index()
            cd['x'] = cd.groupby('y').cumcount() + 1
            cd.reset_index(drop=True, inplace=True)
            cd.rename(columns={'temp_y': 'y'}, inplace=True)
            dfCoor = cd
    
    
            save = st.button("save")
    
            if save:
                st.session_state["button_pressed"] = True
    
                if st.session_state.get("button_pressed", False):
                    prev_year = 2000 + int(YEAR1) - 1
                    year_folder = f'SEASON {prev_year}-{YEAR1}'
                    out_filepath = f'../{year_folder}/03-Canopy Cover/{LOCATION}/'
                    filename = f'{out_filepath}/plotCoordinates.csv'
    
                    if not os.path.exists(out_filepath):
                        os.makedirs(out_filepath)
    
                df = pd.merge(dfMap, dfCoor, on=['x', 'y'])
                df['Location'] = LOCATION
                df['Year'] = YEAR1
                df['Pixels to crop'] = 1300
                df['Rotation'] = 0
                df[['Trial','Plot']] = df['Plot'].str.split('-', expand=True)
                df['Label'] = df['Trial'].astype(str) + '-' + df['Location'].astype(str) + '-' + df['Year'].astype(str) + '-CCP' + '-' + df['Plot'].astype(str)
                df = df[['Location', 'Trial', 'Year', 'Plot', 'Label', 'Latitude','Longitude', 'Pixels to crop', 'Rotation']]
                df.to_csv(filename, index=False)
                st.dataframe(df, hide_index= True, 
                            column_order=('Location', 'Trial', 'Year', 'Plot', 'Label', 'Latitude', 'Longitude'))

    
    with tab2:       
        st.subheader('To generate a kml file, the coordinates must be assigned')

        filtered_data = None  # Initialize filtered_data outside the if statement
    
        if os.path.isfile('metadata/Labels.csv'):
            data = pd.read_csv('metadata/Labels.csv')
            labels = fx.explode_cc_labels(data)    
            col1, col2 = st.columns(2)
            with col1: 
                YEAR = st.selectbox('Year', labels['YEAR'].unique())
            loc_option = labels[(labels['YEAR'] == YEAR)]['LOC_SHORT'].unique()
            with col2:
                LOCATION = st.selectbox('Location', loc_option)
        
        # Construct filepath and read data
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        out_filepath = f'../{year_folder}/03-Canopy Cover/{LOCATION}/'
    
        # Check if out_filepath exists, if not create it
        if not os.path.exists(out_filepath):
            os.makedirs(out_filepath)
    
        filename = f'{out_filepath}/plotCoordinates.csv'
    
        if os.path.isfile(filename):
            data = pd.read_csv(filename)
            st.dataframe(data,
                        )         
            # Filter data based on selected 'Trial' value
        
        TRIAL = st.selectbox('Trial', data['Trial'].unique())
        col1, col2= st.columns(2)
        with col1:
            south = st.number_input("Center Latitude (m) North(-) South(+):", format= '%f')           
        with col2:
            west = st.number_input("Center Longitude (m) East(-) West(+)", format= '%f') 
        if st.button('Filter Data and Generate kml'):
            filtered_data = data[data['Trial'] == TRIAL]
            st.subheader(f"'The Kml file was saved in {out_filepath} as {TRIAL}.kml'")
            st.dataframe(filtered_data)
            df = filtered_data
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
            

    with tab3:
        st.subheader('Rename Photos')
    
        if os.path.isfile('metadata/Labels.csv'):
            data = pd.read_csv('metadata/Labels.csv')
            labels = fx.explode_cc_labels(data)
    
            col1, col2, col3, col4 = st.columns(4)
            with col1: 
                YEAR3 = st.selectbox('Year3', labels['YEAR'].unique())
            loc_option3 = labels[(labels['YEAR'] == YEAR3)]['LOC_SHORT'].unique()
            with col2:
                LOCATION3 = st.selectbox('Location3', loc_option3)
            trial_option3 = labels[(labels['LOC_SHORT'].isin([LOCATION3]))&(labels['YEAR']== YEAR3)]['TRIAL_SHORT'].unique()
            with col3:
                TRIAL3 = st.selectbox('Trial', trial_option3)
                TRIAL3 = [TRIAL3] if isinstance(TRIAL3, str) else TRIAL3
            with col4:
                Feeks = st.selectbox('Feekes', ('F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F10.1', 'F10.5', 'F11.1', 'F11.2', 'F11.3', 'F11.4'))
                
            idx = labels['LOC_SHORT'].isin([LOCATION3]) & labels['TRIAL_SHORT'].isin(TRIAL3) & labels['YEAR'].isin([YEAR3])
            data = labels[idx]
            id_list = data['LABEL'].tolist()
            Plots = data['Plot'].tolist()
            num_ids = len(data)
            missingPlots = st.multiselect('Select the missing plots',Plots)
            if len(missingPlots)>0:
                data = data[~data['Plot'].isin(missingPlots)]
                id_list = data['LABEL'].tolist()
                num_ids = len(data)            
            if st.button('Create Name'):
                st.dataframe(data, hide_index=True,
                             column_order=('LOC_SHORT', 'TRIAL_SHORT',  'YEAR', 'Plot', 'LABEL')) 
            photos = st.text_input('Enter folder path:')            
            rename = st.button("Rename Photos")
        
            if photos:
                if rename:             
                    num_photos = len([name for name in os.listdir(photos) if os.path.isfile(os.path.join(photos, name))])
                    if num_ids == num_photos:
                        files_in_folder = os.listdir(photos)
                        for i, file_name in enumerate(files_in_folder):
                                    old_file_path = os.path.join(photos, file_name)
                                    new_file_path = os.path.join(photos, f'{id_list[i]}.JPG')
                                    os.rename(old_file_path, new_file_path)
                        st.success(f'{num_ids} photos have been renamed')
                    else:
                        st.warning(f'The number of labels ({num_ids}) is not equal to the number of files ({num_photos}) in the folder')     

    with tab4:
        st.title("Image Cropper")
            
        directory_path = st.text_input("Enter directory path:")
    
        if directory_path and os.path.isdir(directory_path):
            files = sorted(os.listdir(directory_path))
    
            repetitions = set()  # Set to store unique repetition numbers
            for file_name in files:
                repetition = file_name.split('-')[4][0]  # Extract first digit of repetition number from file name
                repetitions.add(repetition)
                
            col1, col2 = st.columns(2)
            with col1:
                selected_repetition = st.selectbox("Filter by Repetition", sorted(list(repetitions)))
    
            filtered_files = [file_name for file_name in files if file_name.split('-')[4][0] == selected_repetition]
            
            selected_file_index = st.session_state.get("selected_file_index", 0)
                
            if selected_file_index >= len(filtered_files):
                selected_file_index = len(filtered_files) - 1
            elif selected_file_index < 0:
                selected_file_index = 0
            with col2:
                selected_file = st.selectbox("Select Image", filtered_files, index=selected_file_index)
    
            if selected_file:
                image = cv.imread(os.path.join(directory_path, selected_file))
               
            st.session_state["button_pressed"] = True
    
            if st.session_state.get("button_pressed", False):        
                if selected_file:
                    selected_file = selected_file.replace(".JPG", "")
                    label_split = selected_file.split('-')
                    LOCATION= label_split[1]
                    YEAR = label_split[2]
                    TRIAL = label_split[0].strip()
                    PLOT = label_split[4].strip()   
                                        
                    prev_year = 2000 + int(YEAR) - 1
                    year_folder = f'SEASON {prev_year}-{YEAR}'
                    out_filepath = f'../{year_folder}/03-Canopy Cover/{LOCATION}/'
                    filename = f'{out_filepath}/plotCoordinates.csv'
                                     
                if os.path.isfile(filename):
                    data = pd.read_csv(filename)
                    data['Trial'] = data['Trial'].str.strip()  # Trim whitespace from 'Trial' column
                    data['Plot'] = data['Plot'].str.strip()
                    # Filter data based on both TRIAL and PLOT
                    filtered_data = data[(data['Trial'] == TRIAL) & (data['Plot'] == PLOT)]
                    
                st.data_editor(filtered_data, hide_index =True, 
                                column_order=('Location', 'Trial', 'Year', 'Plot', 'Label', 'Pixels to crop', 'Rotation'),
                              num_rows = 'fixed',
                                disabled = ('Location', 'Trial', 'Year', 'Plot', 'Label'))
                
                top= int(filtered_data['Pixels to crop'])
                
                rotation = int(filtered_data['Rotation'])
                
                col1, col2 = st.columns(2)
                with col1:
                    rotation_angle = st.number_input("Rotation Angle", min_value=-180, max_value=180, value=rotation, step=1, format="%d", key="rotation_angle")  # Text input box for rotation
                with col2:
                    top_text = st.number_input("Top", min_value=50, max_value=2200, value=top, step=30, format="%d", key="top_text")  # Text input box for top value
    
                # Rotate the image based on the provided angle
                rows, cols, _ = image.shape
                rotation_matrix = cv.getRotationMatrix2D((cols/2, rows/2), rotation_angle, 1)
                rotated_image = cv.warpAffine(image, rotation_matrix, (cols, rows))
                save = st.button("Save")
                
                if save:
                    # Update the edited values in the original data
                    data.loc[(data['Trial'] == TRIAL) & (data['Plot'] == PLOT), 'Pixels to crop'] = top_text
                    data.loc[(data['Trial'] == TRIAL) & (data['Plot'] == PLOT), 'Rotation'] = rotation_angle
                    
                    # Write the updated data back to the CSV file
                    data.to_csv(filename, index=False)
                
                # Display the cropped and rotated image
                cropped_image = fx.crop_image(rotated_image, top_text)
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.imshow(cv.cvtColor(cropped_image, cv.COLOR_BGR2RGB))
                ax.axis('off')
                st.pyplot(fig)
                       
        elif directory_path:
            st.write("Invalid directory path. Please enter a valid directory path.")

    if __name__ == "__main__":
        main()

