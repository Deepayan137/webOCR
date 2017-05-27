# -*- coding: utf-8 -*-
import os
import subprocess
import glob
import numpy as np
import cv2
import sys
import random
import shutil
import pandas as pd
#from lookup_intersection import find_different,remove_unicodes
df = pd.read_csv('unicode_table.csv')

from ocr import ocr_ans
def get_features(root,dir):
    lup = []

    Bookcode = str(dir).split('/')[0]
    print root
    ImageFiles = glob.glob(os.path.join(root,dir+'/*.jpg'))

    sortedFiles=sorted(ImageFiles,key=lambda f: int(os.path.splitext(f)[0].split('_')[-1]))

    print sortedFiles
    #print ImageFiles
    ann_folder = (Bookcode+'_annotated_images')
    if os.path.exists(root + ann_folder) == False:
        os.mkdir(root + ann_folder)
    feature_folder= (Bookcode+'_features')
    if os.path.exists(root + feature_folder) == False:
        os.mkdir(root + feature_folder)


    new_list = []
    lookup_file = open('Sanskrit.txt', 'r')
    lookup_text = lookup_file.readlines()
    for i in range(len(lookup_text)):
        new_list.append(lookup_text[i].translate(None, '*\n'))
    #print new_list
    count = 0

    for each_ImageFile in sortedFiles[87:101]:
        count+=1
        PageNo = each_ImageFile.split('-')[-1].split('.')[0]
        print PageNo
        ImagePath = os.path.join(root,each_ImageFile)
        text_file = (ImagePath.split('.')[0] + '.tif.segmentation_plot_file.txt')
        image_name = os.path.basename(ImagePath)
        var = str(image_name)
        featureFile = open(os.path.join(os.path.join(root,feature_folder),image_name)+ '_Features.txt', 'a')
        try:
            image = cv2.imread(ImagePath)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            (rows, cols, chans) = image.shape
            data = np.loadtxt(text_file)
            #print (ImagePath).split('-')[0]+'_'+PageNo+'.tif.txt'
            truth_file=open(ImagePath.split('.')[0]+'.tif.txt')
            #truth_file= open((ImagePath).split('-')[0]+'_'+PageNo+'.tif.txt','r')
            text = truth_file.read()


            lines = text.split('\n')


            #print new_list

            linecount = -1


            for line in lines[:]:
                line = line.decode('utf-8')
                if len(line) > 0:
                    linecount += 1
                    char = []
                    for each_character in line:
                            if each_character == ' ':
                                char.append('0020')

                            elif any(df['character'] == each_character) == True:
                                index = ((np.where(df['character'] == each_character)[0]))
                                #print df['unicode'].iloc[index[0]].translate(None, 'U+')
                                if str(df['unicode'].iloc[index[0]].translate(None, 'U+')) in new_list:
                                    #print df['unicode'].iloc[index[0]].translate(None, 'U+')
                                    char.append(df['unicode'].iloc[index[0]].translate(None, 'U+'))
                            else:
                                #print (each_character.encode("unicode_escape")).translate(None, '\u')
                                if str(each_character.encode("unicode_escape")).translate(None, '\u') in new_list:
                                    #print (each_character.encode("unicode_escape")).translate(None, '\u')
                                    char.append((each_character.encode("unicode_escape")).translate(None, '\u'))
                    a = ' '.join(char)



                    x1 = int(data[linecount][0])
                    y1 = int(data[linecount][1])
                    x2 = int(data[linecount][2]+x1)
                    y2 = int(data[linecount][3]+y1)

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    #cv2.putText(image, str(LineNo), (xcoordoflinenumber,ycoordoflinenumber), font, 1, (0, 255, 0), 2)
                    cv2.putText(image, str(linecount), (x1 - 50, y1 + 25), font, 1, (0, 255, 0), 2)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    line_crop = thresh1[int(y1):int(y2), int(x1):int(x2)]
                    cv2.imwrite(os.path.join(root,ann_folder) + '/' + image_name, image)

                    newHeight = 32
                    aspectRatio = (float(x2 - x1) / float(y2 - y1))

                    newWidth = int(np.ceil(aspectRatio * newHeight))

                    try:
                        resized_image = cv2.resize(line_crop, (int(newWidth), int(newHeight)), interpolation=cv2.INTER_AREA)
                        #cv2.imshow('image',line_crop)
                        #cv2.imshow('image2', resized_image)
                        #cv2.waitKey(0)
                        (cropped_rows, cropped_cols) = resized_image.shape
                    except Exception as e:
                        print (int(newWidth), int(newHeight))
                        print str((x2 - x1)) + '\n' + str(y2 - y1)
                    pixels = []
                    for r in range(cropped_rows):
                        for c in range(cropped_cols):
                            pixel = resized_image[r, c]
                            if pixel == 255:
                                pixels.append(str(1))
                            else:
                                pixels.append(str(0))
                    A = np.array(pixels)
                    B = np.reshape(A, (-1, cropped_cols))
                    # print str(BookCode) + '/' + str(PageNo) + '_' + str(LineNo) +' '+str(newHeight)+' '+str(newWidth)


                    b = ' '.join(pixels)

                # print str(BookCode)+'/'+str(PageNo)+'_'+str(LineNo)+'\n'+str(LineNo)+' '+str(newHeight)+' '+str(newWidth)+' '+b
                    featureFile.write("===Begin==" + "\n")
                    featureFile.write("TAG:" + str(dir) + '/' + str(PageNo) + '_' + str(linecount) + '\n')
                    featureFile.write("TRUTH:" +" "+a+ '\n')
                    #featureFile.write("TRUTH:" + " " + '\n')
                    featureFile.write("FEATURE:" + str(linecount) + ' ' + str(newHeight) + ' ' + str(newWidth) + ' ' + b + '\n')
                    featureFile.write("==END===" + '\n')
        except Exception as e:
            print e
        featureFile.close()
#get_features('/home/deepayan/CVIT_codes/webOCR/multiocr/','fine_tune_Images/')

def combine_text_feat(path,dir,outpath):
    print  dir
    files = glob.glob(os.path.join(path,dir)+'/'+'*.txt' )


    with open(os.path.join(path,outpath), 'a' ) as result:
        for file_ in files:
            for line in open(file_, 'r' ):

                result.write(line )
#combine_text_feat('/home/deepayan/CVIT_codes/webOCR/multiocr/','fine_tune_Images_features/','Bhagavad_features.txt')


def shuffle(path,outFile,book_name):

    train_featureFile = open(os.path.join(path,book_name)+'_trainFile.txt', 'a')
    val_featureFile = open(os.path.join(path,book_name)+'_valFile.txt','a')
    test_featureFile = open(os.path.join(path,book_name)+'_testFile.txt','a')
    tags=[]
    truth=[]
    feat=[]
    a= []
    c=0
    #lookup = open(path + 'lookup/hindi.txt', 'a')
    lines = file(os.path.join(path,outFile)).readlines()
    for each_line in lines:

            words = each_line.split(':')
            if words[0] == 'TAG':
                tags.append(words[1])
            elif words[0] == 'TRUTH':
                truth.append(words[1])
            elif words[0] == 'FEATURE':
                feat.append(words[1])
    print "All lists appended"
    nums = [x for x in range(len(tags))]
    random.shuffle(nums)
    print len(nums)
    train_fr = int(0.6*len(nums))
    val_fr = int(0.8*len(nums))

    mini= min((len(nums)-2000),300)
    print mini



    for i in range(0,2000):
        train_featureFile.write("===Begin==" + "\n")
        train_featureFile.write("TAG:" + tags[nums[i]] + '\n')
        train_featureFile.write("TRUTH:" + truth[nums[i]] + '\n')
        train_featureFile.write("FEATURE:" + feat[nums[i]] + '\n')
        train_featureFile.write("==END===" + '\n')

    train_featureFile.close()
    sum=0
    print "Train File Created"
    for j in range(2000,2000+mini):
        sum+=1
        val_featureFile.write("===Begin==" + "\n")
        val_featureFile.write("TAG:" + tags[nums[j]] + '\n')
        val_featureFile.write("TRUTH:" + truth[nums[j]] + '\n')
        val_featureFile.write("FEATURE:" + feat[nums[j]] + '\n')
        val_featureFile.write("==END===" + '\n')

    print sum
    val_featureFile.close()
    print "Validation File Created"
    for k in range(int(0.8*len(nums)),len(nums)):
        test_featureFile.write("===Begin==" + "\n")
        test_featureFile.write("TAG:" + tags[nums[k]] + '\n')
        test_featureFile.write("TRUTH:" + truth[nums[k]] + '\n')
        test_featureFile.write("FEATURE:" + feat[nums[k]] + '\n')
        test_featureFile.write("==END===" + '\n')

    test_featureFile.close()
    print "Test File created"
#shuffle('/home/deepayan/CVIT_codes/webOCR/multiocr/Bhagavad_features.txt')
def multiocr(path):

    pdf_files = glob.glob('*.pdf')

    #for each_pdf in pdf_files:
     #  print path+each_pdf
      # subprocess.call('./convertpdftotif.sh'+' '+path+each_pdf,shell =True)

    #book_list = [x[0] for x in os.walk(path)]
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            files = os.listdir(dir)
            for each_file in files:
                print  os.path.join(dir,each_file)
                if (os.path.join(dir,each_file)).endswith('jpg') or (os.path.join(dir,each_file)).endswith('tif'):
                    subprocess.call('./j-layout'+' '+os.path.join(dir,each_file),shell=True)
                    os.remove(os.path.join(dir,each_file)+'.blocks.txt')
                    os.remove(os.path.join(dir,each_file)+'.words.txt')

            get_features(root,dir)

#multiocr('/home/deepayan/CVIT_codes/webOCR/multiocr/')



'''def ocr_output():
    language = sys.argv[1]
    feature_folder_path = sys.argv[2]
    output_text_folder = sys.argv[3]
    root = os.path.dirname(feature_folder_path)
    featureFiles = os.listdir(feature_folder_path)


    if os.path.exists(root + output_text_folder) == False:
        os.mkdir(output_text_folder)
    for each_featureFile in featureFiles:
        output_textFile = each_featureFile.split('.jpg_')[0] + '.output.txt'
        # get_ocr_output(each_featureFile,language,output_textFile)
        print os.path.join(feature_folder_path, each_featureFile)
        subprocess.call('./runBLSTM.sh' + ' ' + language + ' ' + os.path.join(feature_folder_path, each_featureFile)
                        + ' ' + output_textFile, shell=True)
        shutil.move(output_textFile, output_text_folder)

#ocr_output()'''

def rename_ocr_output(path):
    files = os.listdir(path)
    for each_file in files:
        PageNo= int(each_file.split('_')[-1].split('.')[0])-1
        print os.path.join(path,'Bhagavad_Gita_%d'%PageNo+'.gt.txt')
        os.rename(os.path.join(path,each_file), os.path.join(path,'Bhagavad_Gita_%d'%PageNo+'.gt.txt'))

def rename_ocr_segfile(path):
    files = os.listdir(path)
    for each_file in files:
        if each_file.endswith('.tif.txt'):
            PageNo = str(each_file.split('Page_')[-1].split('.')[0])
            #print PageNo
        #print os.path.join(path, 'Bhagavad_Gita_%d' % PageNo + '.gt.txt')
            os.rename(os.path.join(path, each_file), os.path.join(path, '3_Bhagavad_Gita_Page_%s' % PageNo + '.jpg.txt'))


#rename_ocr_output('/home/deepayan/CVIT_codes/webOCR/multiocr/Bhagavad_Ground_Truth/')
#rename_ocr_segfile('/home/deepayan/CVIT_codes/webOCR/multiocr/fine_tune_Images')
def get_ocr_score(gt_path,ocr_path):
    gt_files = os.listdir(gt_path)
    ocr_files = os.listdir(ocr_path)
    error=[]
    score =[]
    lines =[]
    for each_gt_file in gt_files:
        gt_PageNo = each_gt_file.split('_')[-1].split('.')[0]
        for each_ocr_file in ocr_files:
            ocr_PageNo = each_ocr_file.split('-')[-1].split('.')[0]
            if gt_PageNo == ocr_PageNo:
                print each_ocr_file,each_gt_file
                s,l =(ocr_ans(os.path.join(ocr_path,each_ocr_file),os.path.join(gt_path,each_gt_file)))
                score.append(s)
                lines.append(l)

    score = np.sum(np.array(s))
    
    character_error =(score/float(lines))*100
    print character_error
    error.append(character_error)
    error = np.array(error)
    mean = np.mean(error)
    print mean

#get_ocr_score('Bhagavad_Ground_Truth/','test_output_2/')
#if __name__ == "__main__":

    #multiocr(sys.argv[1]) #path to directory that contains the pdf
    #get_features(sys.argv[1],sys.argv[2]) #root path and directory that contains the images, segmentation files and output text.
    #combine_text_feat(sys.argv[1],sys.argv[3],sys.argv[4]) #path to root, the directory that conatins
                                                            # the feature files a,d the name of output text file
    #look_up(sys.argv[1])
    #shuffle(sys.argv[1]+sys.argv[4]) #path to where the combined feature files are written
    #rename_ocr_output(sys.argv[5]) #path to directory that conatains OCR output text
    #
    # get_ocr_score('','') # path of directories that contains the ground truth files and OCR output files
