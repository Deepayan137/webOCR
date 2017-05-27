import os
import subprocess
import random
import sys
from parse_sanskrit import copy_files
from multipage_ocr_orig import get_features,combine_text_feat,shuffle
from convert_format import convert
book_ids = {'46':'Siddhi','56':'Deepika','49':'Anubhuti','58':'Sudha'}
#book_ids = {'1504':'1504', '1506':'1506'}
path = sys.argv[1]
language = sys.argv[2]
#root = os.path.basename(path)


def feature_files():
    keys= book_ids.keys()

    for key in keys:
        #print os.path.join(path,book_ids[key])+'/',os.path.join(path,key)+'/'

        #convert(os.path.join(path, key))
        #copy_files(os.path.join(path,book_ids[key])+'/',os.path.join(path,key)+'/')
        print book_ids[key]
        main_dir = book_ids[key]

        feature_dir = os.path.join(path,main_dir+'_features')
        output_file = book_ids[key]+'.FeatOut.txt'
        #get_features(path,main_dir)
        combine_text_feat(path,feature_dir,output_file)

        shuffle(path,output_file,book_ids[key])
        print "completed"
#feature_files()
def combine_all():
    feat_files=[]
    tags = []
    truth = []
    feat = []
    allFeat = open(os.path.join(path,'allFeat.txt'),'w')
    for root, dirs, files in os.walk(path):

        for f in files:
            if f.endswith('.FeatOut.txt'):
                feat_files.append(f)
                print feat_files
    c=0
    for each_file in feat_files:
        lines = file(os.path.join(path, each_file)).readlines()[:2500]
        c+=1
        print c

        for each_line in lines:
            words = each_line.split(':')
            if words[0] == 'TAG':
                tags.append(words[1])
            elif words[0] == 'TRUTH':
                truth.append(words[1])
            elif words[0] == 'FEATURE':
                feat.append(words[1])

    nums = [x for x in range(len(tags))]
    random.shuffle(nums)
    print len(nums)
    for i in range(len(nums)):
        allFeat.write("===Begin==" + "\n")
        allFeat.write("TAG:" + tags[nums[i]] + '\n')
        allFeat.write("TRUTH:" + truth[nums[i]] + '\n')
        allFeat.write("FEATURE:" + feat[nums[i]] + '\n')
        allFeat.write("==END===" + '\n')

    allFeat.close()

'''def train_ocr():
    keys = book_ids.keys()
    for key in keys:
        book_name = book_ids[key]
        try:

                print 'Begining Training for: '+book_name
                subprocess.call('sh runParse_data.sh '+book_name+'> log_error_'+book_name+'.txt',shell=True)

        except Exception as e:
            print e'''

def train_all():
    try:
        subprocess.call('sh run_all_Feat.sh '+path+' '+language,shell=True)
    except Exception as e:
        print e

train_all()



#
if __name__ == "__main__":
    feature_files()
    #train_#ocr()
    combine_all()
