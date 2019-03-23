"""Name:- Triparna Bhattacharya, UIN:- 677270035, CS 582 Assignment 4 """

import os
import re
from nltk.stem import PorterStemmer
import heapq
from collections import defaultdict
import math
import sys

path_gold = sys.argv[1]
path_abstract = sys.argv[2]

stemmer = PorterStemmer()
punctuations='!"#$%&\'()\\n*+,-./:;<=>?@[\\]^`{|}~'
reg_pattern = '[' + punctuations + ']'

stop_words = []
f = open("stopwords.txt")  # the stopwords list provided in the assignment
stop_words = f.read().splitlines()

global_page_rank = {}
vocab_di={}
di = {}
di_tf ={}
di_tf_idf = {}
di2 = {}
di_node_score= {}
top_ten_ngrams = {}
top_ten_words = []
sum_rank=0
result = [0] * 10
top_ten_ngrams_tf_idf ={}
top_ten_words_tf_idf = []

pos_tag = ['nn', 'nns', 'nnp', 'nnps', 'jj']


def preprocess_abstract_file(file_content,file):

        abstract_final = []
        abstract_final1 = []
        for word in file_content.split():
            y = re.sub(reg_pattern, '', word).lower()
            abstract_final.append(str(y))

        for word in abstract_final:
            word_pos_pair = word.split("_")
            if word_pos_pair[1] in pos_tag:
                stemmed_word = stemmer.stem(word_pos_pair[0])
                if stemmed_word not in stop_words:
                    abstract_final1.append(stemmed_word)

            else:
                word = word.replace(word, "")
                abstract_final1.append(word)

        add_graph_node(abstract_final1, file)


def add_graph_node(abstract_final1, file):
    di.clear()
    termfreq = defaultdict(int)
    for word in abstract_final1:
        if (word not in di) & (word != ""):
            di[word] = {}
            dfreq[word] += 1
        termfreq[word] += 1

    termfreq_main[file] = termfreq

    create_vocab_graph(abstract_final1,file)
    for key in di_node_score:
        global_page_rank[key] = di_node_score[key].copy()


dfreq = defaultdict(int)
termfreq_main = defaultdict(int)

def create_vocab_graph(abstract_final1,file):
    vocab_di.clear()
    for index, word in enumerate(abstract_final1):
        new_word_index = index + 1
        if new_word_index < len(abstract_final1):
            word2 = abstract_final1[new_word_index]
            if (word!= "") & (word2 != ""):
                if word in di[word2]:
                    di[word2][word] += 1
                else:
                    di[word2][word] = 1
                if word2 in di[word]:
                    di[word][word2] += 1
                else:
                    di[word][word2] = 1
    vocab_di[file] = di

    node_score(vocab_di,file)
    calculate_bigram_score(abstract_final1, file)
    calculate_trigram_score(abstract_final1, file)

def node_score(vocab_di,file):
    di_node_score.clear()
    di2.clear()
    probability = float(1/len(vocab_di[file]))
    alpha = 0.85
    constant = ((1 - alpha) * (probability))

    for key in di:
        if key not in di2:
            di2[key] = probability
        di_node_score[file] = di2

    for i in range(10):
        for word in vocab_di[file]:
            sum = 0
            for key in vocab_di[file][word]:
                sum += calculate_weight(key, word, file)
            sum = (alpha * sum) + constant
            di_node_score[file][word] = sum

def calculate_weight(key, word, file):

    numerator = vocab_di[file][key][word]
    denominator = 0

    for w in vocab_di[file][key]:
        denominator = denominator + vocab_di[file][key][w]
    score = float(((numerator/denominator) * di_node_score[file][key]))

    return score

def calculate_tf(abstract_final1, file):
    for word in abstract_final1:
        if word != "":
            if word not in di_tf:
                di_tf[word] = {}
            if word in di_tf:
                if file in di_tf[word]:
                    di_tf[word][file] += 1
                else:
                    di_tf[word][file] = 1

def calculate_bigram_score(abstract_final1, file):

        for index, word in enumerate(abstract_final1):
            new_word_index = index + 1
            if new_word_index < len(abstract_final1):
                word2 = abstract_final1[new_word_index]
                if (word != "") & (word2 != ""):
                    bigram_score = float((di_node_score[file][word]) + (di_node_score[file][word2]))
                    di_node_score[file][word, word2] = bigram_score

def calculate_trigram_score(abstract_final1, file):
    top_ten_ngrams.clear()
    top_ten_words.clear()
    for index, word in enumerate(abstract_final1):
        new_word_index = index + 1
        new_word_index2 = new_word_index + 1
        if new_word_index < len(abstract_final1):
            word2 = abstract_final1[new_word_index]
            if new_word_index2 < len(abstract_final1):
                word3 = abstract_final1[new_word_index2]
                if (word != "") & (word2 != "") & (word3 != ""):
                    trigram_score = float((di_node_score[file][word]) + (di_node_score[file][word2]) + (di_node_score[file][word3]))
                    di_node_score[file][word, word2, word3] = trigram_score

    top_ten_ngrams[file] = find_top_ten_ngrams(di_node_score, file)

    for key in top_ten_ngrams[file]:
        top_ten_words.append(key)

    read_gold(file, top_ten_words)

def find_top_ten_ngrams(di_node_score, file):

    score_sorted = dict(heapq.nlargest(10, di_node_score[file].items(), key=lambda x: x[1]))
    return score_sorted

def read_gold(file, top_ten_words):
    
    gold_file_path = "gold/"
    if file in os.listdir(gold_file_path):
        with open(gold_file_path + file, 'r') as f:
            gold_file_content = f.read()
            preprocess_gold_file(gold_file_content, file, top_ten_words)

def preprocess_gold_file(gold_file_content, file, top_ten_words):

    gold_final = []
    for line in gold_file_content.split("\n"):
        stemmed_word=[stemmer.stem(word) for word in line.split()]
        stemmed_word = " ".join(stemmed_word)
        gold_final.append(stemmed_word)


    find_exact_match(gold_final, file, top_ten_words)

def find_exact_match(gold_final, file, top_ten_words):

    rank_list = [0] * 10
    for k in range(1, 11):
        flag = False
        rank_sum = 0
        for key, item in enumerate(top_ten_words[:k]):
            for word in gold_final:
                if type(item) == tuple:
                    item = " ".join(item)
                if item == word:
                    rank = (1/(key+1))
                    rank_sum += rank
                    flag = True
                    break
            if flag:
                break
        rank_list[k-1]=rank_sum
    for ij in range(len(rank_list)-1):
        if rank_list[ij+1] < rank_list[ij]:
            break

    calculate_final_mrr(rank_list)


def calculate_final_mrr(rank_list):
    global result
    mrr_value = [rank * (1/1330) for rank in rank_list]
    result = [x + y for x,y in zip(result, mrr_value)]


tf_idf_main = {}

def calculate_tf_idf():
    for doc in global_page_rank:
        tf_idf = defaultdict(int)
        words = global_page_rank[doc].keys()
        tf_dict = termfreq_main[doc]
        for word in words:
            if type(word) == tuple:
                for tok in word:
                    tf_idf[word] += tf_idf[tok]
            else:
                tf_idf[word] = tf_dict[word] * math.log2(1330 / dfreq[word])
        tf_idf_main[doc] = tf_idf

def calculate_mrr_tf_idf():
    global result
    result = [0] * 10

    for doc in tf_idf_main:
        top_ten_ngrams_tf_idf.clear()
        top_ten_words_tf_idf.clear()
        top_ten_ngrams_tf_idf[doc] = find_top_ten_ngrams(tf_idf_main, doc)
        for key in top_ten_ngrams_tf_idf[doc]:
            top_ten_words_tf_idf.append(key)
        read_gold(doc, top_ten_words_tf_idf)

    for index, value in enumerate(result):

        print ("MRR of Top "  + str(index+1) +  " word using TF-IDF: " + str(value))
    print("")
    print("**********************" + "Process Completed" + "**********************")



def main():
    gold_file_path = path_gold + '/'
    list = os.listdir(gold_file_path)

    path = path_abstract + '/'
    for file in os.listdir(path):
        if file in list[:]:
            with open(path + file, 'r') as f:
                file_content = f.read()

                preprocess_abstract_file(file_content, file)

    for index, value in enumerate(result):
        print ("MRR of Top " + str(index+1) + " word using Page Rank: " + str(value))
    print("")
    print("***********************" + "Comparison " + "***************************")
    print("")

    calculate_tf_idf()
    calculate_mrr_tf_idf()



main()

