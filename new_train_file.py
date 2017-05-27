import  os
import sys
import random
import glob
def extract_sequences(path):
    text_files = os.listdir(path)

    tags = []
    truth = []
    feat = []
    a = []
    c = 0
    for file in text_files:
        with open(os.path.join(path,file),'r') as new_file:
            file_name = file.split('_FeatOut.txt')[0]
            train_featureFile = open(os.path.join(path,file_name+'_train.File.txt'), 'a')

            lines = new_file.readlines()
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

            for i in range(0, 400):
                train_featureFile.write("===Begin==" + "\n")
                train_featureFile.write("TAG:" + tags[nums[i]] + '\n')
                train_featureFile.write("TRUTH:" + truth[nums[i]] + '\n')
                train_featureFile.write("FEATURE:" + feat[nums[i]] + '\n')
                train_featureFile.write("==END===" + '\n')

            train_featureFile.close()
            print "created"



#extract_sequences('/home/deepayan/CVIT_codes/webOCR/multiocr/aall_features')

def combine_text_feat(path,outpath):

    files = glob.glob(path+'/'+'*.File.txt' )


    with open(os.path.join(path,outpath), 'a' ) as result:
        for file_ in files:
            for line in open(file_, 'r' ):

                result.write(line )



if __name__ == "__main__":
    extract_sequences(sys.argv[1])
    combine_text_feat(sys.argv[1],sys.argv[2])

