from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
import numpy as np
import pandas as pd
import string

def get_data(filename):                 #Function to open file and format data
    data = open(filename).read()        
    data = data.split('\n')             #The data set has each review in a new line hence we split with \n

    del data[0]                         #The first line in the dataset is the title "Reviews" sp we remove it
    del data[-1]                        #The last line is an extra empty line so we remove it

    for x in range(len(data)):                                                      #This iterates over the dataset
        data[x] = "".join([ch for ch in data[x] if ch not in string.punctuation])   #Removes all punctuation                      
        data[x] = data[x].replace('"','')                                           #Some review are in quotations so we remove these
        data[x] = data[x].strip().upper().lower()                                   #We remove any whitespaces and convert all data to lowercase

    return data

def get_scores(vsm):                                            #Takes in a Vectorized dataset and calculates and returns a list of scores with the associated word pairs
    X = []
    for i in range(len(vsm.iloc[0])):                           #Iterating for each column
        for j in range(i+1, len(vsm.iloc[0])):                  
            temp = (i,j)                                        #i is the first word and j is the second word, this loop will find the mutual information score of each word with each other word and we store the indices of both the words in a tuple
            temp2 = metrics.mutual_info_score(vsm[i],vsm[j])    #Calculates the mutual information score given two vectors so we gove it the frequecy of two words in each document in the form of a vector 
            temp3 = (temp,temp2)                                #Stores the indices of the 2 words (tuple) and their MI score in another tuple
            X.append(temp3)                                     #Each element in this list take the form of ((x,y),z) where x and y are the indices of the two words in our vectorized dataset and z is their MI score
    
    return X

def get_dataframe(top_pairs):                                   #Takes in a integer n as a parameter and returns a dataframe having the top n associated pairs of words according to their MI scores
    temppairs = []
    for x in range(top_pairs):
        temp = []
        for y in range(2):
            temp.append(vec.get_feature_names()[TopScores[x][0][y]])       #The data in TopScores is in the form ((x,y),z) where x and y are indices of the word pairs in the vectorized dataset vocabulary so we pass x and y to the vocab and store them in a list
        temp.append(TopScores[x][1])                                       #Here we store the score of the word pair
        temppairs.append(temp)                                             
    
    return pd.DataFrame(temppairs, columns = ["Word1","Word2","Score"])


data = get_data("dataset-CalheirosMoroRita-2017.csv")
vec = CountVectorizer(max_features = 15, stop_words='english')      #Converts the dataset into a Vector Space Model. The features have been limited to 15 for ease of computation
output = vec.fit_transform(data)
matrix = output.toarray()                                           

datavec = pd.DataFrame(matrix)                                      #Converts the Vectorized data into a dataframe

X = get_scores(datavec)                                             #Gets the MI score for each pair of words

Scores = []
for i in X:
    Scores.append(i[1])                                             #Creates a list of just the calculated scores

Y = np.argsort(Scores, axis = 0)                                    #Gets a list of indices that sort our scores in ascending order

TopScores = []
for x in range(1,len(X)):                                           #Creates a sorted list of Words pairs and scores in descending order
    num = -x
    TopScores.append(X[Y[num]])

pairs = get_dataframe(50)
pairs.to_csv('mi_scores.txt',sep='\t', index = True)
print("Top 50 word pair associations are: ")
print(pairs.head())



