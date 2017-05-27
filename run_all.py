import os
import sys
import subprocess

books = ['Sudha','Deepika','Siddhi']
def run_all(path):
    for book in books:

        dir_name = os.path.join(path,book+'_ocr_output')
        os.makedirs(dir_name)
        subprocess.call('python multipage_ocr.py'+' '+'Sanskrit'+' '+book+'_features'+' '+dir_name,shell=True)
        subprocess.call('python word_acc_eval'+' '+book+'_ocr_output'+' '+book+'_gt',shell=True)
        os.rmdir()
        subprocess.call('sed -i s/Sanskrit.xml/Sanskrit_'+book+'.xml/g'+' '+'runBLSTM_new.sh',shell=True)
        subprocess.call('python multipage_ocr.py' + ' '+'Sanskrit'+' '+book + '_features' + ' ' +dir_name,shell=True)
        subprocess.call('python word_acc_eval' + ' ' + book + '_ocr_output_new' + ' ' + book + '_gt',shell=True)
        subprocess.call('sed -i s/Sanskrit_'+book+'.xml/Sanskrit_allbooks.xml/g'+' '+'runBLSTM_new.sh',shell=True)
        subprocess.call('python multipage_ocr.py' + ' ' +'Sanskrit'+' '+ book + '_features' + ' ' +dir_name,shell=True)
        subprocess.call('python word_acc_eval' + ' ' + book + '_ocr_output_allbooks' + ' ' + book + '_gt',shell=True)
        subprocess.call('sed -i s/Sanskrit_allbooks.xml/Sanskrit.xml/g'+' '+'runBLSTM_new.sh',shell=True)

run_all('/data5/deepayan/webocr/')