import sys
from collections import defaultdict
import numpy as np
import csv
import argparse
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def NB(testsample,dicts,dictp,dict,prob_num,numwords,numwordp):
    wordsintest ={}
    for x in range(2,len(testsample),2):
        wordsintest[testsample[x]]=int((testsample[x+1]))
    #print wordsintest

    prob=1.0
    wordp=[]
    for word in wordsintest:
        if word in dict:
            #print dict[word]
            fs=0
            fp=0
            if word in dicts:
                fs=dicts[word]
            if word in dictp:
                fp=dictp[word]
            s= float(fs)/numwords
            p= float(fp)/numwordp
            p1= float (s)/(s+p)
            np = float((3 * prob_num) + (dict[word] * p1)) / (3 + dict[word])
            wordp.append(np)
        else :
            p1 = float(3 * prob_num)/ 3
            wordp.append(p1)
    n=1.0
    n1=1.0
    for i in range(len(wordp)):
        n*= wordp[i]
        n1*=(1-wordp[i])
    #print n
    #prob = float(1)/(1+np.exp(n))
    prob=float(n)/(n+n1)

    #print prob
    return prob

def classify_mails():
    spam_list = []
    ham_list = []

    for x in range(len(train_list1)):
        if train_list1[x][1] == 'spam':
            spam_list.append(train_list1[x])

    for x in range(len(train_list1)):
        if train_list1[x][1] == 'ham':
            ham_list.append(train_list1[x])

    total = len(train_list1)
    numspam = len(spam_list)
    numham=len(ham_list)
    #print total
    #print numspam
    #print numham
    #print spam_list
    dict1 = {} # for storing wordcount in spam
    dict2={} # for storing wordcount in ham
    dict={}  #for storing wordcount in entire training data

    #count of words in entire training data
    for i in range(0,len(train_list1)):
        for j in range (2,len(train_list1[i])-1,2):
            if train_list1[i][j] in dict:
                dict[train_list1[i][j]]+= int(train_list1[i][j+1])
            else:
                dict[train_list1[i][j]] = int(train_list1[i][j+1])
    #print "dict word count:", len(dict)
    # count of words in spam list
    for i in range(0,len(spam_list)):
        for j in range(2,len(spam_list[i])-1,2):
            if spam_list[i][j] in dict1:
                dict1[spam_list[i][j]]+= int(spam_list[i][j+1])
            else:
                dict1[spam_list[i][j]] = int(spam_list[i][j+1])

    #print "Spam word count:",len(dict1)
    numwords= 0
    for i in dict1:
       numwords += dict1[i]

    # count of word in ham list
    for i in range(0,len(ham_list)):
        for j in range(2,len(ham_list[i])-1,2):
            if ham_list[i][j] in dict2:
                dict2[ham_list[i][j]]+= int(ham_list[i][j+1])
            else:
                dict2[ham_list[i][j]] = int(ham_list[i][j+1])
    #print "Ham word count:", len(dict2)
    numwordp = 0
    for i in dict2:
        numwordp += dict2[i]

    # implementation of naive bayes :
    prob_spam= float(numspam)/total
    #print prob_spam
    prob_ham = float(numham) / total
    #print prob_ham
    """
    spam_prob = NB(test_list1[0], dict1,dict2, numspam, prob_spam)
    ham_prob = NB(test_list1[0], dict2,dict1, numham, prob_ham)
    if(spam_prob> ham_prob):
        print "spam"
    else:
        print "ham"
    """
    outputl = []
    with open(args['o'], 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE)
        for x in test_list1:
            spam_prob=NB(x,dict1,dict2,dict,prob_spam,numwords,numwordp)
            #print spam_prob
            ham_prob=NB(x,dict2,dict1,dict,prob_ham,numwords,numwordp)
            #print ham_prob
            if(spam_prob > ham_prob):
                filewriter.writerow([x[0],'spam'])
                outputl.append('spam')
            else:
                filewriter.writerow([x[0],'ham'])
                outputl.append('ham')



    output= csv.reader(open('output.csv','rb'))


    accuracy = getAccuracy(test_list1,outputl)
    print "Accuracy=",accuracy

parser = argparse.ArgumentParser()
parser.add_argument('-f1', help='training file in csv format', required=True)
parser.add_argument('-f2', help='test file in csv format', required=True)
parser.add_argument('-o', help='output labels for the test dataset', required=True)

args = vars(parser.parse_args())
# input from the command line
if __name__ == '__main__':
    # print len(sys.argv)


    train_file = args['f1']
    test_file = args['f2']

    # open and read the datasets
    train_list = []
    test_list = []
    train_list1 = []
    test_list1 = []

    # read the train data
    train = open(train_file)
    for line in train:
        for word in line.splitlines():
            train_list.append(word)

    train_list = np.array(train_list)

    # print train_list

    for x in range(len(train_list)):
        str = train_list[x]
        words = str.split(" ")
        train_list1.append(words)

    # print train_list1[0][1]

    # read the test data
    test = open(test_file)
    for line in test:
        for word in line.splitlines():
            test_list.append(word)

    test_list = np.array(test_list)

    for x in range(len(test_list)):
        str = test_list[x]
        words = str.split(" ")
        test_list1.append(words)

    # print test_list1[3][1]

    classify_mails()

