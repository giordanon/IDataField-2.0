def explode_labels(inData):
    
    """
    input: 
    output:
    This function is for...
    """
    import pandas as pd
    from numpy import arange
    
    inData = inData.dropna().reset_index()
    inData['SAMPLING'] = inData['SAMPLING'].str.replace(' ', '').str.split(pat = ",",  expand = False)
    inData['Trt1'] = pd.Series(dtype = 'object')
    inData['Rep1'] = pd.Series(dtype = 'object')
    
    for k,row in inData.iterrows():
        inData.at[k,'Trt1'] = arange(1,int(inData.at[k,'TRT'])+1)
        inData.at[k,'Rep1'] = arange(1,int(inData.at[k,'REPS'])+1)
            
    df = inData.explode('SAMPLING').explode('Rep1').explode('Trt1')
    df['Plot'] = df['Rep1'] * 100 + df['Trt1']
    df['LABEL'] = df['TRIAL_SHORT'].astype(str) + '-' + df['LOC_SHORT'].astype(str) + '-' + df['YEAR'].astype(str) + '-' + df['SAMPLING'].astype(str) + '-' + df['Plot'].astype(str)
    df = df.reset_index()
    #df.to_csv("labels.csv", index = False)
    return df

def label_generator(data, SIZE, FILENAME, out_filepath):
    import os, qrcode, time
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from PyPDF2 import PdfFileReader, PdfFileWriter
    
    data = data
    size = SIZE[0] 
    filename = FILENAME

    output = PdfFileWriter()

    if size == 'BIG':
        h = 2.4
        w = 3.9
        y = -0.70 * inch
        x = 0.67 * inch
        txt_size = 15
        y2 = 9
        x2 = 1.1 * inch
        qrsize = 2.2
        qrx = 0.3 * inch
        qry = -0.5 * inch
    elif size == 'SMALL':
        h = 1.4
        w = 3.5
        y = -0.7 * inch
        x = - 0.3 * inch
        txt_size = 12
        y2 = - 0.1 * inch
        x2 = 0.01 * inch
        qrsize = 1.6
        qrx = 0.45 * inch
        qry = -0.9 * inch

    for labels in data.index[0:]:
        label = data['LABEL'][labels]
        c = canvas.Canvas(f"{out_filepath}pdf1.pdf", pagesize=(w*72, h*72))

        height = h * inch
        width = w * inch

        c.translate(inch,inch)
        # Define font type and size
        c.setFont("Helvetica", txt_size)


        c.setStrokeColorRGB(1,1,1)
        c.setFillColorRGB(0,0,0)
        # Draw label
        c.drawString(y, x , f"{label}")
        c.setFont("Helvetica", 15)
        c.drawString(y2,x2 , "@KSU_WHEAT")

        # Draw a QR code
        img = qrcode.make()

        qr = qrcode.QRCode(version = 1,
                           error_correction = qrcode.constants.ERROR_CORRECT_H,
                           box_size = qrsize,
                           border = 4)

        qr.add_data(label)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        c.drawInlineImage(image = img, x = qrx , y = qry, preserveAspectRatio = True)
        # Save file
        c.showPage()
        c.save()
        time.sleep(.1)
        pdfOne = PdfFileReader(f"{out_filepath}pdf1.pdf", "rb")
        output.add_page(pdfOne.pages[0])
        time.sleep(.1)
        
    outputStream = open(f"{out_filepath}{filename}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    time.sleep(.1)

def explode_plot_labels(inData): 
    import pandas as pd
    from numpy import arange
    
    data = inData.dropna().reset_index()
    data['SAMPLING'] = data['SAMPLING'].str.replace(' ', '').str.split(pat = ",",  expand = False)
    data['Trt1'] = pd.Series(dtype = 'object')
    data['Rep1'] = pd.Series(dtype = 'object')

    for k,row in data.iterrows():
        data.at[k,'Trt1'] = arange(1,int(data.at[k,'TRT'])+1)
        data.at[k,'Rep1'] = arange(1,int(data.at[k,'REPS'])+1)

    df = data.explode('SAMPLING').explode('Rep1').explode('Trt1')
    df['Plot'] = df['Rep1']*100 + df['Trt1']
    df['LABEL'] = df['TRIAL_SHORT'].astype(str) + '-' + df['LOC_SHORT'].astype(str) + '-' + df['YEAR'].astype(str) + '-' + df['SAMPLING'].astype(str) + '-' + df['Plot'].astype(str)
    df = df.reset_index() 
    return df 

def directory_check(ID):
    import os
    
    TRIAL,SITE, YEAR, SAMPLING, PLOT = ID.split('-')
    
    prev_year = 2000 + int(YEAR) - 1
    year_folder = f'SEASON {prev_year}-{YEAR}'
    folder_path = f'../{year_folder}/01-Data/{TRIAL}'
    filename = f'{folder_path}/{TRIAL}.csv'
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    tempOut = [filename, TRIAL, SITE, YEAR, SAMPLING, PLOT]
    return(tempOut)


def directory_check_combine(YEAR, TRIAL):
    import os
    
    prev_year = 2000 + int(YEAR) - 1
    year_folder = f'SEASON {prev_year}-{YEAR}'
    folder_path = f'../{year_folder}/01-Data/{TRIAL}'
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    filename = f'{folder_path}/{TRIAL}_Combine_Data.csv'
    
    return(filename)

def file_check_combine(LOCATION, filename, merged_data):
    import os
    import pandas as pd
    import streamlit as st
    
    if os.path.isfile(filename):
        temp1 = pd.read_csv(filename)
        
        if LOCATION in temp1['LOCATION'].unique():
            st.write(f'{LOCATION} already added.')
            
        if not LOCATION in temp1['LOCATION'].unique():
            tempOut = pd.concat([temp1, merged_data])
            tempOut.to_csv(filename, index = False)
        
    if not os.path.isfile(filename):
        merged_data.to_csv(filename, index = False)


    

def upload_partitioning(ID, TRAITS, WEIGHTS):
    import pandas as pd
    import os
    import functions as fx
    
    filename, TRIAL, SITE, YEAR, SAMPLING, PLOT = fx.directory_check(ID)

    if not os.path.isfile(f'{filename}'): 
        df_create = pd.DataFrame(columns = ['ID', 'TRAIT', 'VALUE', 'TRIAL','SITE', 'YEAR', 'SAMPLING', 'PLOT'])
        df_create.to_csv(filename, index = False)      

    df = pd.read_csv(filename)
    
    for i in range(len(TRAITS)):
        values_to_add = pd.DataFrame({'ID': [ID], 
                                      'TRAIT': [TRAITS[i]],
                                      'VALUE':[WEIGHTS[i]], 
                                      'TRIAL':[TRIAL], 
                                      'SITE':[SITE], 
                                      'YEAR':[YEAR], 
                                      'SAMPLING':[SAMPLING], 
                                      'PLOT':[PLOT]})
        
        df = pd.concat([df, values_to_add], ignore_index=True)
    
    df.to_csv(filename, index = False)
    df = pd.read_csv(filename)

    return df

def count_seeds(image, GRAIN_WEIGHT):
    
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    from skimage.color import rgb2gray, label2rgb
    from skimage.filters import threshold_otsu
    from skimage.morphology import area_opening, disk, binary_closing
    from skimage.measure import find_contours
    
    RGB = mpimg.imread(image)
    I = rgb2gray(RGB)
    # Apply Otsu's method
    global_threshold  = threshold_otsu(I)
    BW = I < global_threshold
    #Smoothing 
    #Remove small areas
    BW = area_opening(BW, area_threshold = 1000, connectivity=2)
    # CLosing operation (Connects small patches of True pixels)
    BW = binary_closing(BW, disk(5))
    contours = find_contours(BW,0)
    seed_num = len(contours)
    TKW = (GRAIN_WEIGHT/seed_num)*1000 #introduce fx for defining tkw 

    plt.imshow(BW, cmap = 'gray')
    plt.axis('off')
    for contour in contours:
        plt.plot(contour[:,1], contour[:,0], '-r', linewidth = 1)
    plt.savefig('tempImage.jpg')
    
    return TKW

## Metadata functions
def add_metatrials(TRIAL_LONG, TRIAL_SHORT):
    import os
    import pandas as pd
    
    filename = 'metadata/Trials.csv'
    if not os.path.isfile(filename): 
        df_create = pd.DataFrame(columns = ['Trial Name', 'TRIAL_SHORT', 'TRIAL_CODE'])
        df_create.to_csv(filename, index = False) 


    values_to_add = pd.DataFrame({'Trial Name': [TRIAL_LONG], # select box 
                                  'TRIAL_SHORT': [TRIAL_SHORT], #Select box - single trial
                                  'TRIAL_CODE': [999]})

    df = pd.read_csv(filename)
    dfnew = pd.concat([df, values_to_add], ignore_index=True)
    dfnew.to_csv(filename, index = False)

## Function to add new locations
def add_metalocations(LOCATION, LOC_SHORT):  
    import os
    import pandas as pd
    
    filename = 'metadata/Locations.csv'
    if not os.path.isfile(filename): 
        df_create = pd.DataFrame(columns = ['Location', 'LOC_SHORT'])
        df_create.to_csv(filename, index = False) 


    values_to_add = pd.DataFrame({'Location': [LOCATION], 
                                  'LOC_SHORT': [LOC_SHORT]})

    df = pd.read_csv(filename)
    dfnew = pd.concat([df, values_to_add], ignore_index=True)
    dfnew.to_csv(filename, index = False)
    
## Function to add new traits
def add_metatraits(TRAIT, TRAIT_SHORT):  
    import os
    import pandas as pd
    
    filename = 'metadata/Traits.csv'
    if not os.path.isfile(filename): 
        df_create = pd.DataFrame(columns = ['TRAIT', 'TRAIT_SHORT'])
        df_create.to_csv(filename, index = False) 


    values_to_add = pd.DataFrame({'TRAIT': [TRAIT], 
                                  'TRAIT_SHORT': [TRAIT_SHORT]})

    df = pd.read_csv(filename)
    dfnew = pd.concat([df, values_to_add], ignore_index=True)
    dfnew.to_csv(filename, index = False)
    
def add_metactivity(ACTIVITY, ACTIVITY_SHORT):
    import os
    import pandas as pd
    
    filename = 'metadata/Activities.csv'
    if not os.path.isfile(filename): 
        df_create = pd.DataFrame(columns = ['ACTIVITY', 'ACTIVITY_SHORT'])
        df_create.to_csv(filename, index = False) 


    values_to_add = pd.DataFrame({'ACTIVITY': [ACTIVITY], 
                                  'ACTIVITY_SHORT': [ACTIVITY_SHORT]})

    df = pd.read_csv(filename)
    dfnew = pd.concat([df, values_to_add], ignore_index=True)
    dfnew.to_csv(filename, index = False)

## Add trial within a field and sampling
def add_metalabels(TRIAL, LOCATION, YEAR, TRT, REPS, SAMPLING, TRIAL_CODE = 9999):
    import os
    import pandas as pd
    
    filename = 'metadata/Labels.csv'
    if not os.path.isfile(filename): 
        df_create = pd.DataFrame(columns = ['YEAR', 'TRIAL_SHORT','LOC_SHORT','TRT','REPS','SAMPLING','TRIAL_CODE'])
        df_create.to_csv(filename, index = False)
    
    values_to_add = pd.DataFrame({'YEAR': YEAR, # select box 
                                  'TRIAL_SHORT': TRIAL, #Select box - single trial
                                  'LOC_SHORT':LOCATION, # Multiple locations
                                  'TRT':TRT, # Number of treatments of the trial
                                  'REPS':REPS, # Number of replicates of the trial, make sure you have the same reps ax selected locations
                                  'SAMPLING':[SAMPLING], 
                                  'TRIAL_CODE':[TRIAL_CODE]})

    df = pd.read_csv(filename)
    dfnew = pd.concat([df, values_to_add], ignore_index=True)
    dfnew.to_csv(filename, index = False)
    
# Update samplings
def update_samplings(values_to_add, TRIAL_SHORT, YEAR, LOC_SHORT):
    
    import pandas as pd
    
    filename = 'metadata/Labels.csv'
    data = pd.read_csv(filename)
    # Select a trial to update sampling
    filtered = data[data['TRIAL_SHORT'].isin([TRIAL_SHORT]) & data['YEAR'].isin([YEAR]) & data['LOC_SHORT'].isin([LOC_SHORT])]['SAMPLING']
    sampling = filtered.str.replace(' ', '').str.split(pat = ",",  expand = False)
    out = []
    [out.extend(inner_list) for inner_list in sampling]
    # Out object contains updatdata sampling values 
    out += values_to_add
    # Convert list to string ans separate samplign times with a comma
    out = ', '.join(out)
    # Add updates sampling into the old dataframe
    condition = data['TRIAL_SHORT'].isin([TRIAL_SHORT]) & data['YEAR'].isin([YEAR]) & data['LOC_SHORT'].isin([LOC_SHORT])
    data.loc[condition, 'SAMPLING'] = out
    data.to_csv(filename, index = False)
    
    return(data)