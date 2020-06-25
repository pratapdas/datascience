#Importing the required libraries
import pandas as pd
import itertools
import time

#Please uncomment the below code snippet (10 - 12) to take inputs from console

#Taking the required files and values as input from the user

#docword_path = input("Enter the path for the DOCWORD file: ")
#vocab_path = input("Enter the path for the VOCAB file: ")
#K = int(input("Enter the value of K (as in K-frequent itemsets): "))

#Selecting the 'kos' input file as input
docword_path = 'docword.kos.txt'
vocab_path = 'vocab.kos.txt'
K = 3

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

#Creating the list of transactions and support count
transactions = []
support = {}
for i in range(D):
    transactions.append([])
for i in range(W):
    support[vocab_data['word'].iloc[i]] = 0
for i in range(NNZ):
    transactions[int(data['docID'].iloc[i])-1].append(vocab_data['word'].iloc[int(data['wordID'].iloc[i])-1])
    support[vocab_data['word'].iloc[int(data['wordID'].iloc[i])-1]] += (1/D)


#Generating the MIS values    
mis = {}
for k in support.keys():
    if support[k] < (100/D):
        mis[k] = 2
    else:
        mis[k] = 0.9 * support[k]
 
#Sorting out the mis dicitionary according to it's values
mis = {k: v for k, v in sorted(mis.items(), key=lambda item: item[1])}

#Generating items which are atleast greater than the minimum of all MIS values
L = []
min_mis = 0.0
for k in mis.keys():
    if (support[k] >= mis[k]) and min_mis == 0.0:
        min_mis = mis[k]
        L.append(k)
    elif min_mis != 0.0:
        if (support[k] >= min_mis):
            L.append(k)
    


def generate_F1_itemsets(L,levels,support,mis,transactions, sdc):
    F1 = []
    for item in L:
        if (support[item] >= mis[item]):
            F1.append(item)
    print('Length of candidate set of 1 itemset = ', len(F1), '\n')
    print("Frequent itemsets of size 1: \n")
    for item in F1:
        print(item,end=',')
    generate_item_sets(F1,levels,support,mis,transactions, sdc)
    

def generate_item_sets(L,levels,support,mis,transactions, sdc):
    k = 2
    freq_item_set = []
    Ck_count_dict = {}
    while (k == 2 or k <= levels):
        if k == 2:
            Ck = level2_candidate_gen(L, sdc, support, mis, transactions)
            for c in Ck:
                Ck_count_dict.update({str(c): 0})
        else:
            Ck = MScandidate_gen(freq_item_set, sdc, support, mis, transactions)
        print('\n', 'Length of candidate set of %d itemset = %d' %(k,len(Ck)), '\n')
        for t in transactions:
            for c in Ck:
                if (set(c).issubset(set(t))):
                    if (Ck_count_dict.get(str(c))):
                        Ck_count_dict[str(c)] += 1
                    else:
                        Ck_count_dict.update({str(c): 1})        
        freq_item_set = []
        for c in Ck:
            if (float(Ck_count_dict[str(c)] / D) >= mis[c[0]]):
                freq_item_set.append(c)
        print("Frequent itemsets of size {}:".format(k) , '\n')
        for item in freq_item_set:
            print(item,end=',')
        k += 1

def level2_candidate_gen(L, sdc, support, mis, transactions):
    c2 = []
    for l in range(len(L)):
        l_mis = 0.0
        l_supp = 0.0
        if support[L[l]] >= mis[L[l]]:
            l_mis = mis[L[l]]
            l_supp = support[L[l]]
            for h in range(l + 1, len(L)):
                if ((support[L[h]] >= l_mis) and (abs(support[L[h]] - l_supp) <=  sdc)):
                    c2.append([L[l], L[h]])
    return(c2)

def MScandidate_gen(freq_item_set, sdc, support, mis, transactions):
	Ck = []
	f1 = []
	f2 = []
	for i in range(len(freq_item_set)):
		f1 = freq_item_set[i][0:-1]
		for j in range(i + 1, len(freq_item_set)):
			f2 = freq_item_set[j][0:-1]
			if (f1 == f2) and (abs(support[freq_item_set[i][-1]] - support[freq_item_set[j][-1]]) <=  sdc):
				temp_list = list(freq_item_set)
				c1 = list(temp_list[i])
				c2 = temp_list[j][-1]
				c1.append(c2)
				Ck.append(c1)
	i = 0
	while i < len(Ck):
		subsets = list(itertools.combinations(Ck[i], len(Ck[i]) - 1))
		for s in subsets:
			s = list(s)
			if (Ck[i][0] in s) or (mis[Ck[i][1]] == mis[Ck[i][0]]):
				if s not in freq_item_set:
					Ck.remove(Ck[i])
		i += 1
	return Ck

    
generate_F1_itemsets(L,K,support,mis,transactions,1e-4)

#Noting the end time
end_time = time.time()

print()
print('The execution time was:', end_time-start_time)

    
    
    
    
    
    
    
    
    
    
    
    

    



    




































