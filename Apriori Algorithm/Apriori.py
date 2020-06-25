#Importing the required libraries
import pandas as pd
from apyori import apriori
import time

#Please uncomment the below code snippet (10 - 13) to take inputs from console

#Taking the required files and values as input from the user

#docword_path = input("Enter the path for the DOCWORD file: ")
#vocab_path = input("Enter the path for the VOCAB file: ")
#K = int(input("Enter the value of K (as in K-frequent itemsets): "))
#F = float(input("Enter the value of minimum support: "))

#Selecting the 'kos' input file as input
docword_path = 'docword.kos.txt'
vocab_path = 'vocab.kos.txt'
K = 3
F = 0.15

#Noting the start time
start_time = time.time()

#Importing the DOCWORD file and extracting required information
dataset = pd.read_csv(docword_path, sep = "\t", header = None)
D = int(dataset.iloc[[0][0]][0])
W = int(dataset.iloc[[1][0]][0])
NNZ = int(dataset.iloc[[2][0]][0])

#Modifying the dataframe to easily convert it into a list of transactions
data = dataset.iloc[3:]
data = data[0].str.split(expand=True)
data.reset_index(drop = True)
data.columns = ['docID', 'wordID', 'count']

#Importing the VOCAB file
vocab_data = pd.read_csv(vocab_path, sep = "\t", header = None)
vocab_data.columns = ['word']

#Creating the list of transactions
transactions = []
for i in range(D):
    transactions.append([])
for i in range(NNZ):
    transactions[int(data['docID'].iloc[i])-1].append(data['wordID'].iloc[i])

#Calling the apriori function to list all frequent itemsets whose support >= F
results = list(apriori(transactions, min_support=F))

#Printing the required K-itemsets for which minimum support >= F
count = 0
for i in range(len(results)-1,-1,-1):
    result = list(results[i][0])
    for j in range(len(result)):
        result[j] = vocab_data.iloc[int(result[j])][0]
    if(len(result)==K):
        print(result)
        count += 1

if count == 0:
    print()
    print("There are no " + str(K) + "-frequent itemsets for a minimum supprot value of " + str(F) + ".")
else:
    print()
    print("There are " + str(count) + " " + str(K) + "-frequent itemsets for a minimum supprot value of " + str(F) + ".")

#Noting the end time
end_time = time.time()

print('The execution time was:', end_time-start_time)