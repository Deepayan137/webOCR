import cv2
import os
import subprocess
from PIL import Image
import pandas as pd
import numpy as np
df = pd.read_csv('unicode_table.csv')
def convert(path):

    for dirname, dirnames, filenames in os.walk(path):

        #for subdirname in dirnames:

         #   for _, _, files in os.walk(os.path.join(dirname, subdirname)):
        for file in filenames:

            if file.endswith('.TIF') or file.endswith('.tif') or file.endswith('.tif.fixed.jpg'):
                filepath = (os.path.join(dirname, file))

                new_imageName = file.split(".")[0] + '.jpg'
                image = Image.open(filepath)
                print new_imageName
                #image = cv2.imread(filepath)
                image.save(os.path.join(path,new_imageName))




#convert('/home/deepayan/CVIT_codes/webOCR/multiocr/46/')
def read_text(ImagePath):
    lup=[]
    #text_file= open(ImagePath+'.txt','r')
    text_file = open(ImagePath,'r')
    text = text_file.read()
    lines = text.split('\n')


    linecount = -1
    for line in lines[:]:
        line = line.decode('utf-8')

        # print len(line)
        if len(line) > 0:
            linecount += 1
            char = []
            for each_character in line:

                if each_character == ' ':
                    char.append('0020')
                    lup.append(char)
                elif any(df['character'] == each_character) == True:
                    index = ((np.where(df['character'] == each_character)[0]))
                    char.append(df['unicode'].iloc[index[0]].translate(None, 'U+'))
                    lup.append(char)

                else:
                    char.append((each_character.encode("unicode_escape")).translate(None, '\u'))
                    lup.append(char)
            a = ' '.join(char)

            print a
#read_text('/home/deepayan/CVIT_codes/webOCR/multiocr/fine_tune_Images/14_0038.tif.txt')