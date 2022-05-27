from asyncio import selector_events
import warnings
warnings.filterwarnings("ignore")

import cv2
import numpy as np
from tensorflow.python.keras.layers import Input, Dense
from tensorflow.python.keras.models import Sequential
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
from PIL import Image,ImageOps
import segmentor as segmentor
import matplotlib.pyplot as plt
import os
import shutil
# 'segmented' directory contains each mathematical symbol in the image
root = os.getcwd()
if 'segmented' in os.listdir():
    shutil.rmtree('segmented')
os.mkdir('segmented')
SEGMENTED_OUTPUT_DIR = os.path.join(root, 'segmented')
# trained model
MODEL_PATH = os.path.join(root, 'model1.tf')
# csv file that maps numerical code to the character
mapping_processed = os.path.join(root, 'mapper.csv')

def img2emnist(filepath, char_code):
    img = Image.open(filepath).resize((45, 45))
    inv_img = ImageOps.invert(img)
    flatten = np.array(inv_img).flatten() / 255
    flatten = np.where(flatten > 0.5, 1, 0)
    csv_img = ','.join([str(num) for num in flatten])
    csv_str = '{},{}'.format(char_code, csv_img)
    return csv_str

def processor(INPUT_IMAGE):
    img = Image.open(INPUT_IMAGE)
    # segmennting each character in the image
    segmentor.image_segmentation(INPUT_IMAGE)
    segmented_images = []
    files = sorted(list(os.walk(SEGMENTED_OUTPUT_DIR))[0][2])
    # writing images to the 'segmented' directory
    for file in files:
        file_path = os.path.join(SEGMENTED_OUTPUT_DIR , file)
        segmented_images.append(Image.open(file_path))

    files = sorted(list(os.walk(SEGMENTED_OUTPUT_DIR))[0][2])
    for file in files:
        filename = os.path.join(SEGMENTED_OUTPUT_DIR, file)
        img = cv2.imread(filename, 0)

        kernel = np.ones((2,2), np.uint8)
        dilation = cv2.erode(img, kernel, iterations = 1)
        cv2.imwrite(filename, dilation)
        
    model = load_model(MODEL_PATH)
    parsed_str=''
    #classes = ['(', ')', '+', ',', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'C', 'X', 'cos', 'd', 'div', 'forward_slash', 'int', 'log', 'sin', 'sqrt', 'tan', 'y', 'z']
    classes = ['(', ')', '+', ',', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'C', 'X', 'c', 'd', 'div', 'forward_slash', 'int', 'l', 's', 'sqrt', 't', 'y', 'z']
    #classes = [')', '2'] 
    
    segmented_characters = 'segmented_characters.csv' 
    if segmented_characters in os.listdir():
        os.remove(segmented_characters)
    # resize image to 48x48 and write the flattened out list to the csv file
    with open(segmented_characters, 'a+') as f_test:
        column_names = ','.join(["label"] + ["pixel" + str(i) for i in range(784)])
        print(column_names, file=f_test)
        count = 0
        files = sorted(list(os.walk(SEGMENTED_OUTPUT_DIR))[0][2])
        for f in files:
            file_path = os.path.join(SEGMENTED_OUTPUT_DIR, f)
            # print(f'FIlEPATH: {file_path}')
            img = cv2.imread(file_path,cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, dsize =(45, 45), interpolation = cv2.INTER_AREA)
            # print(img.shape)
            img = np.reshape(img,[1,45,45,1])
            results = model.predict(img)[0]
            # f = open("bracket.txt","a")
            # f.write("\n" + str(entropy))
            # print(f"Entropy of ) = {results[1]}")
            # print(f"Entropy of 2 = {results[7]}")
            # print(f"Entropy difference = {results[7]-results[1]}")
            max_r = np.argmax(results)
            selected_class = classes[max_r]
            if selected_class == 'd':
                count+=1
            if count == 0:
                if f[0] == '2':
                    parsed_str += ';'
                    count += 1
            
            print("SELECTED CLASS="+selected_class)
            if selected_class in [')','2']:
                
                entropy = results[7]-results[1]
                if entropy>=5:
                    parsed_str += classes[7]
                else:
                    parsed_str += classes[1]
            elif selected_class in ['(','C']:
                parsed_str += classes[0]
            else:
                parsed_str += classes[max_r]
            print(f'Parsed string: {parsed_str}')
            #print(csv, file=f_test)

    #test_df = data = pd.read_csv('segmented_characters.csv')
    #X_data = data.drop('label', axis = 1)
    #X_data = X_data.values.reshape(-1,45,45,1)
    #X_data = X_data.astype(float)

    df = pd.read_csv(mapping_processed)
    code2char = {}
    for index, row in df.iterrows():
        code2char[row['id']] = row['char']
    # predict each segmented character
    #results = np.argmax(results, axis = 1)
    #parsed_str = ""
    #for r in results:
    #    max_r = np.argmax(r)
    #    #parsed_str += code2char[r]
    #    parsed_str += classes[max_r]
    #print(f'Parsed string: {parsed_str}')
    return parsed_str

def main(operationBytes):
    Image.open(operationBytes).save('input.png')
    equation = processor('input.png')
    print('\nequation :', equation)
    return equation
