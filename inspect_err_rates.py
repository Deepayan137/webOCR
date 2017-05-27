#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import codecs
import sys

import os
import pandas as pd
import re
import numpy as np


from matplotlib import pyplot as plt
def txt_to_csv(path,outfile):
    log_file = open(path,'r')
    log_text = log_file.read()

    ler = re.findall(r'labelErrorRate(.*?)\n',log_text)
    insertions = re.findall(r'insertions(.*?)\n',log_text)
    deletions = re.findall(r'deletions(.*?)\n',log_text)
    substitutions = re.findall(r'substitutions(.*?)\n',log_text)

    mydict = {'labelErrorrate':ler[:-1],
              'insertions':insertions[:-1],
              'deletions':deletions[:-1],
              'substitutions':substitutions[:-1]}

    df = pd.DataFrame.from_dict(mydict)
    df.to_csv(outfile)

def get_labels(path):
    out_lineno = []
    out_label=[]
    tar_label = []
    train_ler = []
    val_ler = []
    tar_lineno = []
    mydict = {}
    #pattern = re.compile("output label string",re.IGNORECASE)
    #pattern2 = re.compile("target label string",re.IGNORECASE)
    pattern = re.compile("train errors ", re.IGNORECASE)
    pattern2 = re.compile("calculating validation errors",re.IGNORECASE)
    with open(path) as in_file:
        for linenum, line in enumerate(in_file):

            #mydict[linenum] =line.replace('\n','0020')
            mydict[linenum] = line.translate(None,'\t\n')

            if pattern.search(line.translate(None,'\t\n')) != None:

                out_lineno.append((linenum))
            if pattern2.search(line.translate(None,'\t\n')) != None:
                tar_lineno.append((linenum))

    for i in range(len(out_lineno)):

        #out_label.append(mydict[(out_lineno[i]+1)])
        #tar_label.append(mydict[(tar_lineno[i]+1)])
        train_ler.append(mydict[(out_lineno[i]+4)])
        val_ler.append(mydict[(tar_lineno[i]+4)])



    return(train_ler,val_ler)
def plot_lers():
    mylist = ['Anubhuti','Deepika']
    #print mydidct[mydidct.keys()[2]]
    #print len(mylist)
    for k in range(len(mylist)):
        print mylist[k]
        train,val = get_labels('/home/deepayan/CVIT_codes/webOCR/multiocr/log_error_%s.txt'%mylist[k])

        ler=[]
        #print mydidct[mydidct.keys()[k]]
        #txt_to_csv('/home/deepayan/CVIT_codes/webOCR/multiocr/val_err_rate.txt','finetuned_validation_error_rate.csv')
        for i in range(len(train)):
            ler.append([train[i].split(' ')[1],(val[i].split(' ')[1])])
        df2 = pd.DataFrame(ler,columns=['train ler','val ler'])
        df2.to_csv('ler.csv')
        df = pd.read_csv('ler.csv')
        index = df.index.values
        train_ler = df['train ler'].tolist()

        val_ler = df['val ler'].tolist()

        print np.min(np.array(train_ler))
        print np.min(np.array(val_ler))
        plt.figure()
        p1 = plt.plot(index, train_ler, color='b')
        p2  = plt.plot(index,val_ler,color = 'r')
        plt.ylabel('Label Error Rate')
        plt.xlabel('Epochs')
        plt.title('Training and validation label Error rates')

        plt.legend((p1[0],p2[0]),('Training Label error Rate','Validation Label Error rate'))
        #var = mydidct[mydidct.keys()[k]]
        #print var

        plt.savefig('Plot_single_%s.png'%mylist[k])

        print 'done'
plot_lers()
def plot_df(start,end):
    df1 = pd.read_csv('validation_error_rate.csv')
    df2 = pd.read_csv('finetuned_validation_error_rate.csv')
    index = np.arange(end-start)

    plt.xticks(rotation=45)
    ler1 = df1['labelErrorrate'][start:end]

    ler2 = df2['labelErrorrate'][start:end]

    max_ler1 = np.max(np.array(ler1))
    max_ler2 = np.max(np.array(ler2))
    l = max([max_ler1,max_ler2], key=lambda x: int(x))
    '''p1 = plt.bar(index, ler1, color='b')
    p2  = plt.bar(index,ler2,color = 'r')
    plt.ylabel('Label Error Rate')
    plt.title('Comparison of Label Error Rates')
    plt.xticks(np.arange(0,len(index),2))
    plt.yticks(np.arange(0,l,10))
    plt.legend((p1[0],p2[0]),('Before Finetuning','After Finetuning'))
    plt.savefig('labelerror.png')'''
    list2=[]
    for i in range(len(df1['labelErrorrate'])):
        if df1['labelErrorrate'].iloc[i]+df2['labelErrorrate'].iloc[i] >100 \
                and abs(df1['labelErrorrate'].iloc[i]-df2['labelErrorrate'].iloc[i]) < 5:
            list2.append(i)
            #print i,df1['labelErrorrate'].iloc[i],df2['labelErrorrate'].iloc[i]
    #print list2
    #list2.append(30)
    tar,out = get_labels('val_err_rate.txt')
    fileid = open('compare.txt','a')
    #print tar[28]+'\n'+out[28]+'\n'
    #print len(tar)
    char=[]
    new_df = df2.drop(df2.index[list2])
    new_ler = np.array(new_df['labelErrorrate'])
    mean_ler = np.mean(new_ler)
    print mean_ler
    for k in range(len(list2)):

        tr = tar[list2[k]].split(' ')
        x = '\u'+'\u'.join(tr)
        encoded = x.encode('utf-8')
        pr = out[list2[k]].split(' ')

        y = '\u'+'\u'.join(pr)

        pr_encoded = y.encode('utf-8')

        #print (encoded.decode('unicode-escape'))
        #print encoded
        #x = x.decode('unicode-escape')


        try:
            text = (encoded.decode('unicode-escape'))
            pr_text = pr_encoded.decode('unicode-escape')
            fileid.write('target:'+text.encode('utf-8')+'\n'+'output:'+pr_text.encode('utf-8')+'\n')


        except Exception as e:
            print e
        a = np.zeros(shape=(len(tr),len(pr)))
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                if tr[i] == pr[j]:
                    a[i][j] =1
        df = pd.DataFrame(a,index=tr,columns=pr)
        #df.to_csv('conf_matrix_%d.csv'%k)

    fileid.close()

#plot_df(150,200)

'''s= u'\u0020\u092e\u093e\u0939\u002D'
encoded = s.encode('utf-8')
print encoded
file = open('out.txt','w')
file.write(encoded)
file.close()'''
#get_labels('/home/deepayan/CVIT_codes/webOCR/multiocr/val_err_rate.txt')
