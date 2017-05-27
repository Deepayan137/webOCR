from bs4 import BeautifulSoup
import re
import os
from PIL import Image
import subprocess
from shutil import copy,move
prefix = '<br />'
suffix = '<br />'
path = '/home/deepayan/CVIT_codes/webOCR/multiocr/'
all_files = os.listdir(path)
def add_prefix():

    for each_file in all_files[3:]:
        if each_file.endswith('.gt.txt'):
            source_file = (open(path+each_file,'r'))

            fname = (path+each_file).split('gt.txt')[0]+'gt1'+'.txt'
            #print fname
            dest_text = (open(fname,'w'))
            text = source_file.read()
            dest_text.write('%s%s%s\n' % (prefix, text, suffix))
            os.remove(path + each_file)
#add_prefix()
def convert(path):

    for dirname, dirnames, filenames in os.walk(path):

        #for subdirname in dirnames:

         #   for _, _, files in os.walk(os.path.join(dirname, subdirname)):
        for file in filenames:
            print file
            if file.endswith('.TIF') or file.endswith('.tif'):
                filepath = (os.path.join(dirname, file))

                new_imageName = file.split(".")[0] + '.jpg'
                image = Image.open(filepath)

                #image = cv2.imread(filepath)
                image.save(path+new_imageName)
#convert('/home/deepayan/CVIT_codes/webOCR/multiocr/51/')
def parse_lines():
    for each_file in all_files[:]:
        if each_file.endswith('.gt1.txt'):
            print each_file
            source_file = (open(path + each_file, 'r'))
            fname = (path+ each_file).split('.gt1.txt')[0] + '.gt.txt'
            dest_text = (open(fname, 'a'))
            text = source_file.read()
            #print text.decode('utf-8')
            lines = re.findall(r'<br />(.+?)<br />',text)
            #print len(lines)

            for each_line in lines:
                #print each_line.decode('utf-8')
                dest_text.write(each_line+'\n')
            dest_text.close()
            os.remove(path + each_file)

#parse_lines()

def copy_files(path1,path2):

    files = os.listdir(path1)

    image_files = os.listdir(path2)
    #print image_files
    #subprocess.call('rm -rf'+' '+os.path.join(path2+'*.segmentation_plot_image.jpg'),shell=True)

    for file in files:
        PageNo = file.split('.')[0].split('_')[1]
        #print PageNo
        for img_file in image_files:
            img_PageNo = img_file.split('.')[0].split('_')[1]

            try:
                if PageNo == img_PageNo:
                    #print path2+img_file,path1
                    #move(path2+img_file,'Anu/')
                    #copy(os.path.join(path2,img_file),path2)
                    if img_file.endswith('.jpg')==1 and img_file.endswith('.segmentation_plot_image.jpg')==0 and \
                            img_file.endswith('.tif.fixed.jpg')== 0 :
                        copy(os.path.join(path2,img_file),path1)

                    if img_file.endswith('.txt'):
                        copy(os.path.join(path2,img_file),path1)


            except Exception as e:
                print e


#copy_files('new/Siddhi/','new/46/')
