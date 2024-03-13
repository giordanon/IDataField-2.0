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
        inData.at[k,'Trt1'] = arange(1,int(inData.at[k,'Trt'])+1)
        inData.at[k,'Rep1'] = arange(1,int(inData.at[k,'Reps'])+1)
            
    df = inData.explode('SAMPLING').explode('Rep1').explode('Trt1')
    df['Plot'] = df['Rep1'] * 100 + df['Trt1']
    df['LABEL'] = df['TRIAL_SHORT'].astype(str) + '-' + df['LOC_SHORT'].astype(str) + '-' + df['YEAR'].astype(str) + '-' + df['SAMPLING'].astype(str) + '-' + df['Plot'].astype(str)
    df = df.reset_index()
    df.to_csv("labels.csv", index = False)
    return df

def label_generator(data, SIZE, FILENAME, out_filepath):
    import os, qrcode, time
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from PyPDF2 import PdfReader, PdfWriter
    
    data = data
    size = SIZE[0] 
    filename = FILENAME

    output = PdfWriter()

    if size == 'BIG':
        h = 2.4
        w = 3.9
        y = -0.5*inch
        x = 0.67*inch
        txt_size = 20
        y2 = 9
        x2 = 1.1*inch
        qrsize = 3
        qrx = 0.1 * inch
        qry = -0.9*inch
    elif size == 'SMALL':
        h = 1.4
        w = 3.5
        y = -0.5 * inch
        x = - 0.3 * inch
        txt_size = 15
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
        pdfOne = PdfReader(f"{out_filepath}pdf1.pdf", "rb")
        output.add_page(pdfOne.pages[0])
        time.sleep(.1)
        
    outputStream = open(f"{out_filepath}{filename}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

def explode_plot_labels(inData): 
    import pandas as pd
    from numpy import arange
    
    data = inData.dropna().reset_index()
    data['SAMPLING'] = data['SAMPLING'].str.replace(' ', '').str.split(pat = ",",  expand = False)
    data['Trt1'] = pd.Series(dtype = 'object')
    data['Rep1'] = pd.Series(dtype = 'object')

    for k,row in data.iterrows():
        data.at[k,'Trt1'] = arange(1,int(data.at[k,'Trt'])+1)
        data.at[k,'Rep1'] = arange(1,int(data.at[k,'Reps'])+1)

    df = data.explode('SAMPLING').explode('Rep1').explode('Trt1')
    df['Plot'] = df['Rep1']*100 + df['Trt1']
    df['LABEL'] = df['TRIAL_SHORT'].astype(str) + '-' + df['LOC_SHORT'].astype(str) + '-' + df['YEAR'].astype(str) + '-' + df['SAMPLING'].astype(str) + '-' + df['Plot'].astype(str)
    df = df.reset_index() 
    return(df)

def upload_partitioning(ID, TRAIT, TRAIT_2, TRAIT_3, TRAIT_4, MASS, MASS_2, MASS_3, MASS_4):
    import pandas as pd
    import os
    TRIAL,SITE, YEAR, SAMPLING, PLOT = ID.split('-')
        
    prev_year = 2000 + int(YEAR) - 1
    year_folder = f'SEASON {prev_year}-{YEAR}'
    folder_path = f'../{year_folder}/01-Data/{TRIAL}'

    filename = f'{folder_path}/{TRIAL}.csv'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.path.isfile(f'{filename}'): 
        df_create = pd.DataFrame(columns = ['ID', 'TRAIT', 'VALUE', 'TRIAL','SITE', 'YEAR', 'SAMPLING', 'PLOT'])
        df_create.to_csv(filename, index = False)      

    df = pd.read_csv(filename)


    values_to_add = {'ID': [ID], 'TRAIT': [TRAIT], 'VALUE':[MASS], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}
    values_to_add_2 = {'ID': [ID], 'TRAIT': [TRAIT_2], 'VALUE':[MASS_2], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}
    values_to_add_3 = {'ID': [ID], 'TRAIT': [TRAIT_3], 'VALUE':[MASS_3], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}
    values_to_add_4 = {'ID': [ID], 'TRAIT': [TRAIT_4], 'VALUE':[MASS_4], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}

    df_new = pd.DataFrame(values_to_add)
    df_new_2 = pd.DataFrame(values_to_add_2)
    df_new_3 = pd.DataFrame(values_to_add_3)
    df_new_4 = pd.DataFrame(values_to_add_4)

    df = pd.concat([df, df_new, df_new_2, df_new_3, df_new_4])
    df.to_csv(filename, index = False)

    df = pd.read_csv(filename)

    return(df)