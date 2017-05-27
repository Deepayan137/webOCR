import os,sys
import subprocess
import numpy as np
def word_acuracy_evaluation(corrected_file,ocr_out_file):
    correctfile = open(corrected_file, 'r')
    correct_text = correctfile.read()
    correct_text = correct_text.decode('utf-8')
    ocrfile = open(ocr_out_file, 'r')
    ocr_text = ocrfile.read()
    ocr_text = ocr_text.decode('utf-8')
    #cmd = ['/home/webocr/ocr-evaluation-tools/dist/bin/ocrevalutf8.fix', 'wordacc', corrected_file, ocr_out_file]
    process = subprocess.check_output('/home/webocr/ocr-evaluation-tools/dist/bin/ocrevalutf8.fix'
                                      +' '+'wordacc'+' '+ocr_out_file+' '+corrected_file)


    accuracy = process.splitlines()[4].strip().split()[0].replace('%', '')
    if accuracy == '------':
        accuracy = 100.0

    return accuracy
def ocr_files():
    ocr_out_folder = sys.argv[1]
    correted_ocr_folder = sys.argv[2]
    s =[]
    ocr_out_folder_files = os.listdir(ocr_out_folder)
    correted_ocr_folder_files = os.listdir(correted_ocr_folder)
    for corrected_file in correted_ocr_folder_files:
        corrected_file_PageNo = corrected_file.split('.')[0]
        for ocr_out_file in ocr_out_folder_files:
            ocr_out_file_PageNo = ocr_out_file.split('.')[0]
            if corrected_file_PageNo == ocr_out_file_PageNo:
                s.append(word_acuracy_evaluation(os.path.join(correted_ocr_folder,corrected_file)
                                                 ,os.path.join(ocr_out_folder,ocr_out_file)))
    score = np.mean(np.array(s))
    return score,ocr_out_folder.split('/')[-1].split('_')[0]
fileid = open('wordaccuracy.txt','a')
score,book_name=ocr_files()
text = book_name+':'+score
fileid.write(text)