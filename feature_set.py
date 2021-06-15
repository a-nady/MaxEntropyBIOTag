import sys
from nltk.stem import PorterStemmer
import os
stemmer = PorterStemmer()

#first argument is file name
#second argument is if its trained or not (0 or 1)
def parse(file, train):
    try:
        # open file from terminal
        data = open(file, 'r').read()
    except:
        print(file + " was not found or cannot be read.")
        sys.exit(1)
    #split by line
    arr = data.split('\n')

    set = []
    newset = []
    for i in range(len(arr)):
        if len(arr[i]) == 0:
            continue
        arr[i] = arr[i].split("\t")

    for j in range(len(arr)):
        if len(arr[j]) == 0:
            set.append("")
            continue
        temp = featurize(j, arr)
        set.append(temp)

    #similarize(set)

    #if its a training file add 3rd entry from array
    if (train == 1):
        prevBIO = "O"
        for i in range(len(set)):
            if len(set[i]) != 0:
                set[i].append("prevBIO=" + prevBIO)
                set[i].append(arr[i][2])
                prevBIO = arr[i][2]
            
    return set

def featurize(i, set):
    
    newa = []
    word = set[i][0]
    pos = set[i][1]

    #initializing features
    prev_word = "N/A"
    prev_wordpos = "N/A"
    prevprev_word = "N/A"
    prevprev_wordpos = "N/A"

    next_word = "N/A"
    next_wordpos = "N/A"
    nextnext_word = "N/A"
    nextnext_wordpos = "N/A"

    # prevent OOB exception
    # gathering features
    if (i != 0):
        if (len(set[i - 1]) != 0):
            prev_word = set[i - 1][0]
            prev_wordpos = set[i - 1][1]
            # prevent OOB exception
            if (i - 1 != 0):
                if (len(set[i - 2]) != 0):
                    prevprev_word = set[i - 2][0]
                    prevprev_wordpos = set[i - 2][1]

    if (len(set[i + 1]) != 0):
        next_word = set[i + 1][0]
        next_wordpos = set[i + 1][1]
        if len(set[i + 2]) != 0:
            nextnext_word = set[i + 2][0]
            nextnext_wordpos = set[i + 2][1]

    stemmed = stemmer.stem(word)
    cap = "NO"
    end = "NO"
    beg = "NO"

    #see if capatalized
    if word[0].isupper():
        cap = "YES"

    if prev_word == "N/A":
        beg = "YES"
    if next_word == "N/A":
        end = "YES"

    EndsInS = "NO"
    if word[len(word)-1] == "s":
        EndsInS = "YES"
    
    newa = [word, "POS=" + pos, "Stemmed_Word="+stemmed, "Capitalized="+cap, "EndsInS="+EndsInS, "Prev_Word=" + prev_word, "Next_Word=" + next_word, "Prev_WordPOS=" + prev_wordpos,"PrevPrev_WordPOS=" + prevprev_wordpos, "Next_WordPOS=" + next_wordpos,  "NextNext_WordPOS=" + nextnext_wordpos]

    return newa

'''
def comparefeature(arr1, arr2):
    c = 0
    for i in range(len(arr1)):
        if arr1[i] == arr2[i]:
            c += 1
    return c

def similarize(set):
    newset = []
    for i in range(len(set)):
        if len(set[i]) == 0:
            newset.append("")
            continue
        
        prev_similar = "N/A"
        prevprev_similar = "N/A"
        next_similar = "N/A"
        nextnext_similar = "N/A"

        a1 = set[i]
        
        if a1[3] != "Prev_Word=N/A":
            a2 = set[i - 1]
            prev_similar = comparefeature(a1, a2)
        if a1[5] != "PrevPrev_Word=N/A":
            a2 = set[i - 2]
            prevprev_similar = comparefeature(a1, a2)
        if a1[7] != "Next_Word=N/A":
            a2 = set[i + 1]
            next_similar = comparefeature(a1, a2)
        if a1[9] != "NextNext_Word=N/A":
            a2 = set[i + 2]
            nextnext_similar = comparefeature(a1, a2)
            
        newset.append(set[i])
        newset[i].extend(["Prev_Similar="+str(prev_similar), "PrevPrev_Similar="+str(prevprev_similar), "Next_Similar="+str(next_similar), "NextNext_Similar="+str(nextnext_similar)])
'''

def write_file(set, name):
    w = open(name, "w")

    i = 0
    while True:
        if i == len(set) - 1:
            break
        
        j = 0
        while True:
            if (j ==  len(set[i])):
                break
            
            w.write(set[i][j])
            j += 1
            
            if (j ==  len(set[i])):
                break
            w.write( '\t')
            
            

        w.write('\n')
        i += 1

test_arr = parse(sys.argv[1], 0)
train_arr = parse(sys.argv[2], 1)

write_file(test_arr, 'test.feature')
write_file(train_arr, 'training.feature')

print("Feature files created.")