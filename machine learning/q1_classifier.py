import random
import pickle as pkl
import argparse
import csv
import math
import numpy as np
from scipy import stats

'''
TreeNode represents a node in your decision tree
TreeNode can be:
    - A non-leaf node: 
        - data: contains the feature number this node is using to split the data
        - children[0]-children[4]: Each correspond to one of the values that the feature can take
        
    - A leaf node:
        - data: 'T' or 'F' 
        - children[0]-children[4]: Doesn't matter, you can leave them the same or cast to None.

'''

# DO NOT CHANGE THIS CLASS
class TreeNode():
    def __init__(self, data='T',children=[-1]*5):
        self.nodes = list(children)
        self.data = data

    def save_tree(self,filename):
        obj = open(filename,'w')
        pkl.dump(self,obj)

def save_tree(self,filename):
        obj = open(filename,'w')
        pkl.dump(self,obj)
        
# loads Train and Test data
def load_data(ftrain, ftest,fname):
    Xtrain, Ytrain, Xtest, attrname = [],[],[],[]
    with open(ftrain, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = map(int,row[0].split())
            Xtrain.append(rw)

    with open(ftest, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = map(int,row[0].split())
            Xtest.append(rw)

    ftrain_label = ftrain.split('.')[0] + '_label.csv'
    with open(ftrain_label, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = int(row[0])
            Ytrain.append(rw)
            
    with open(fname, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = row[0]
            attrname.append(rw)
    print('Data Loading: done')
    return Xtrain, Ytrain, Xtest, attrname


num_feats = 274

#A random tree construction for illustration, do not use this in your code!
def create_random_tree(Xtrain_data, attr_name, depth):
    vals = [record[len(Xtrain_data[0]) - 1 ] for record in Xtrain_data]

    if len(attr_name) <= 0 or len(Xtrain_data) == 0:
        frequency = {}
        for rows in Xtrain_data:
            if (frequency.has_key(rows[len(Xtrain_data[0])-1])):
                frequency[rows[len(Xtrain_data[0])-1]] += 1 
            else:
                frequency[rows[len(Xtrain_data[0])-1]] = 1
        max = 0
        max_freq = ""
        for key in frequency.keys():
            if frequency[key]>max:
                max = frequency[key]
                max_freq = key
        return TreeNode(numToString(max_freq),[])
    elif vals.count(vals[0]) == len(vals):
        return TreeNode(numToString(vals[0]),[])
    else:
        next_attribute = 0;
        info_gain = 0;
        #print(len(Xtrain_data[0])-1)
        #print(len(attr_name))
     
        for i in range(len(Xtrain_data[0])-1):
            temp = informationGain(Xtrain_data, i, len(Xtrain_data[0]) - 1) 
            if temp>info_gain:
                info_gain = temp
                next_attribute = i
        #dummy tree created for testing. 
        dt = {next_attribute:{}}    
        #print(next_attribute)
        #feat = random.randint(0,273)
        root = TreeNode(str(next_attribute))
        if chiTest(next_attribute, Xtrain_data) == 0:
             frequency = {}
             for rows in Xtrain_data:
                if (frequency.has_key(rows[len(Xtrain_data[0])-1])):
                    frequency[rows[len(Xtrain_data[0])-1]] += 1 
                else:
                    frequency[rows[len(Xtrain_data[0])-1]] = 1
             max = 0
             max_freq = ""
             for key in frequency.keys():
                if frequency[key]>max:
                     max = frequency[key]
                     max_freq = key
             return TreeNode(numToString(max_freq),[]) 
        #print(attr_name.pop(next_attribute))
        i = 0;
        for val in range(5):
            new_data = removeClassifiedData(Xtrain_data, next_attribute, val)
            #print(np.asarray(new_data).shape)
            attr_nam = attr_name[:]
            #new_data = np.delete(Xtrain_data,next_attribute, 1)
            attr_nam.pop(next_attribute)
            #new_data = Xtrain_data[np.where(Xtrain_data[:,next_attribute] == val)]
            #print(np.asarray(new_data).shape)          
            root.nodes[val] = create_random_tree(new_data,attr_nam,depth+1)
    return root 

def chiTest(next_attribute, Xtrain_data):

    statistic_inter = 0.0
    chi_pob_value = 0.0
    for value in np.unique([row[next_attribute] for row in Xtrain_data]):
        total_true = 0.0
        total_false = 0.0
        total_true_p = 0.0
        total_false_p = 0.0
        attr_true = 0
        attr_false = 0
        attr_true_p = 0.0
        attr_false_p = 0.0

        distinct_val = np.unique([row[next_attribute] for row in Xtrain_data])
        for row in Xtrain_data:
            if (row[next_attribute] == value):
                if (row[len(Xtrain_data[0])-1]) == 0:
                    attr_false += 1
                else:
                    attr_true += 1
            if (row[len(Xtrain_data[0])-1] == 0):
                total_false+=1
            else:
                total_true+=1
                
        attr_true_p = float(attr_true) * float(len(Xtrain_data)) / float(len(Xtrain))
        attr_false_p = float(attr_false) * float(len(Xtrain_data)) / float(len(Xtrain))
        total_true_p = float(total_true) / float(len(Xtrain_data))
        total_false_p = float(total_false) / float(len(Xtrain_data))
        s_p = 0.0
        s_n = 0.0
        if attr_true_p <> 0 and attr_false_p <> 0:
            s_p = float((math.pow((attr_true_p-total_true_p),2))/float(attr_true_p))
            s_n = float((math.pow((attr_false_p-total_false_p),2))/float(attr_false_p))
        s_t = s_p + s_n    
        statistic_inter += s_t        
    chi_pob_value = float(1) - float(stats.chi2._cdf(statistic_inter,1))
    if(chi_pob_value > pval):
        return 0
    return 1;

def numToString(val):
    return 'T' if val==1 else 'F'
    
def attributeEntropy(training_data, label_attr):
    entropy = 0.0
    distinct_attribute = {}
    for row in training_data:
        if (distinct_attribute.has_key(row[label_attr])):
            distinct_attribute[row[label_attr]] += 1.0
        else:
            distinct_attribute[row[label_attr]]  = 1.0
            
    for prob in distinct_attribute.values():
        entropy += (-prob/len(training_data)) * math.log(prob/len(training_data), 2) 

    return entropy


def evaluate_datapoint(root,datapoint):
    if root.data == 'T': return 1
    if root.data =='F': return 0
    return evaluate_datapoint(root.nodes[datapoint[int(root.data)-1]-1], datapoint)

def informationGain(training_data, attribute, label):
    value_numbers = {}
    entropy_data = 0.0 
    for row in training_data:
        if (value_numbers.has_key(row[attribute])):
            value_numbers[row[attribute]] += 1.0
        else:
            value_numbers[row[attribute]]  = 1.0

    for attrData in value_numbers.keys():
        data = [record for record in training_data if record[attribute] == attrData]
        entropy_data += value_numbers[attrData] / sum(value_numbers.values()) * attributeEntropy(data, label) 
        
    return (attributeEntropy(training_data, label) - entropy_data)

def removeClassifiedData(training_data, attribute, value):

    left_data = [[]]
    for row in training_data:
        if (row[attribute] == value):
            newRow = []
            for i in range(0,len(row)):
                if(i != attribute):
                    newRow.append(row[i])
            left_data.append(newRow)

    left_data.remove([])    
    return left_data

parser = argparse.ArgumentParser()
parser.add_argument('-p', required=True)
parser.add_argument('-f1', help='training file in csv format', required=True)
parser.add_argument('-f2', help='test file in csv format', required=True)
parser.add_argument('-o', help='output labels for the test dataset', required=True)
parser.add_argument('-t', help='output tree filename', required=True)

args = vars(parser.parse_args())

pval = args['p']
Xtrain_name = args['f1']
Ytrain_name = args['f1'].split('.')[0]+ '_labels.csv' #labels filename will be the same as training file name but with _label at the end

Xtest_name = args['f2']
Ytest_predict_name = args['o']

tree_name = args['t']

attributes_name = "featnames.csv"

dt = {}
Xtrain, Ytrain, Xtest, attrname = load_data(Xtrain_name, Xtest_name,attributes_name )

print("Training...")

labelled_data =  np.insert(Xtrain, len(Xtrain[0]), Ytrain, axis=1)
s = create_random_tree(labelled_data,attrname, 0)

print("Testing...")
Ypredict = []

root = pkl.load(open('tree.pkl','r'))
for i in range(0,len(Xtest)):
    Ypredict.append([evaluate_datapoint(root,Xtest[i])])

with open(Ytest_predict_name, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(Ypredict)

print("Output files generated")









