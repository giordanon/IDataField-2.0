import streamlit as st
import pandas as pd
import os
import functions as fx

def app():
    
    with st.expander("New trial"):
        TRIAL_LONG = st.text_input('Insert the full name of the trial', key=1)
        TRIAL_SHORT = st.text_input('Insert short name of the trial', 
                                    help = 'Maximum number of digits is 5. Special characters (",",".","-") are not allowed. Case sensitive.',
                                    key = 2,
                                    max_chars = 5)
        if st.button(f'Load {TRIAL_SHORT}', key='b1'):
            try: 
                fx.add_metatrials(TRIAL_LONG, TRIAL_SHORT)
                st.write(f'{TRIAL_SHORT} loaded successfully!')
            except:
                st.error('Error message')
                st.write('Make sure you did not changed metadata file names.')           
            
    with st.expander("New location"):
        LOCATION = st.text_input('Insert the full name of the location',key=3)
        LOC_SHORT = st.text_input('Insert short name of the location', 
                                  help = 'Maximum number of digits is 5. Special characters (",",".","-") are not allowed. Case sensitive.',
                                  key=4,
                                  max_chars = 5)
        
        if st.button(f'Load {LOC_SHORT}', key='b2'):
            try: 
                fx.add_metalocations(LOCATION, LOC_SHORT)
                st.write(f'{LOC_SHORT} loaded successfully!')
            except:
                st.error('Error message')
                st.write('Make sure you did not changed metadata file names.')
                
    with st.expander("New traits"):
        TRAIT = st.text_input('Enter full name of the trait',key=5)
        TRAIT_SHORT = st.text_input('Insert short name of the trait', 
                                    help = 'Maximum number of digits is 3. Special characters (",",".","-") are not allowed. Case sensitive.',
                                    key=6,
                                    max_chars = 3)
        
        if st.button(f'Load {TRAIT}', key='b3'):
            try: 
                fx.add_metatraits(TRAIT, TRAIT_SHORT)
                st.write(f'{TRAIT_SHORT} loaded successfully!')
            except:
                st.error('Error message')
                st.write('Make sure you did not changed metadata file names.')
    
    with st.expander("New activity"):
        ACTIVITY = st.text_input('Decribe the activity',key=7, max_chars = 20)
        ACTIVITY_SHORT = st.text_input('Insert short name for the activity', 
                                       help = 'Maximum number of digits is 5. Special characters (",",".","-") are not allowed. Case sensitive.',
                                       key=8,
                                       max_chars = 5)
        
        if st.button(f'Load {TRAIT}', key='b4'):
            try: 
                fx.add_metactivity(ACTIVITY, ACTIVITY_SHORT)
                st.write(f'{ACTIVITY_SHORT} loaded successfully!')
            except:
                st.error('Error message')
                st.write('Make sure you did not changed metadata file names.')
                
    with st.expander("Experimental design"):
        trials = pd.read_csv('metadata/Trials.csv')
        locations = pd.read_csv('metadata/Locations.csv')
        traits = pd.read_csv('metadata/Traits.csv')
        pheno = ['F010', 'F020', 'F030', 'F040', 'F050' ,'F060' ,'F070' ,'F080' ,'F090' ,'F010' ,'F101' ,'F105' ,'F111' ,'F112' ,'F113' ,'F114']
        traits = pd.read_csv('metadata/Traits.csv')
        
        col1, col2, col3 = st.columns(3)
        
        with col1: 
            TRIAL = st.selectbox('Trial', trials['TRIAL_SHORT'].unique(), key = 100)
        with col2: 
            LOCATION = st.selectbox('Location', locations['LOC_SHORT'].unique(), key = 200)
        with col3:
            YEAR = st.number_input('Harvest year of the trial', min_value = 2010, max_value = 2100, step=1, placeholder = 2024)
            YEAR = YEAR - 2000
            
        col4, col5, col6 = st.columns(3)
        
        with col4:
            PHENO = st.multiselect('Select sampling phenology', pheno, key = 300)
        with col5:
            TRAITS = st.multiselect('Select sampling traits', traits['TRAIT'].unique(), key = 400)
            TRAITS = traits[traits['TRAIT'].isin(TRAITS)]['TRAIT_SHORT']
            
        with col6:
            combined = [x + '_' + y for x in PHENO for y in TRAITS]
            SAMPLING = st.multiselect('Crop stage x Trait', combined)
            SAMPLING = ', '.join(SAMPLING)
            
        col7, col8 = st.columns(2)
            
        with col7:
            TRT = st.number_input('Number of treatments', min_value = 1, step=1)
        with col8:
            REPS = st.number_input('Number of replicates', min_value = 1, step=1)
        
        if st.button(f'Load {TRIAL} in {LOCATION}', key='b5'):
            try: 
                fx.add_metalabels(TRIAL, LOCATION, YEAR, TRT, REPS, SAMPLING, TRIAL_CODE = 9999)
                st.write(f'{YEAR} - {TRIAL} - {LOCATION} loaded successfully!')
            except:
                st.error('Complete all fields above')
             
    with st.expander("Add additional sampling to trial within a field"):
        data = pd.read_csv('metadata/Labels.csv')
        
        col1, col2, col3 = st.columns(3)
        
        with col1: 
            TRIAL = st.selectbox('Trial', data['TRIAL_SHORT'].unique(), key = 500)
        with col2: 
            LOCATION = st.selectbox('Location', data['LOC_SHORT'].unique(), key = 600)
        with col3:
            YEAR = st.selectbox('Year', data['YEAR'].unique(), key = 700)
            
        col4, col5, col6 = st.columns(3)
        
        with col4:
            PHENO = st.multiselect('Select sampling phenology', pheno, key = 800)
        with col5:
            TRAITS = st.multiselect('Select sampling traits', traits['TRAIT'].unique(), key =900)
            TRAITS = traits[traits['TRAIT'].isin(TRAITS)]['TRAIT_SHORT']
            
        with col6:
            combined = [x + '_' + y for x in PHENO for y in TRAITS]
            SAMPLING = st.multiselect('Crop stage x Trait', combined, key = 1000)
            
        if st.button(f'Update sampling for {TRIAL} in {LOCATION}', key='b6'):
            try: 
                fx.update_samplings(SAMPLING, TRIAL, YEAR, LOCATION)
            st.write(f'Samplings for {YEAR} - {TRIAL} - {LOCATION} updated! You can now print labels you need!')
            except:
                st.error('Complete all fields above. Output filename is metadata/Labels.csv, make sure the file is in the correct directory.')
        
    
        
        
        
        
    