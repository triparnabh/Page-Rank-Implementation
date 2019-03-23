# Page-Rank-Implementation
Page Rank Implementation with POS tagged documents

=======================================================================

Name:- TRIPARNA BHATTACHARYA, UIN: 677270035, Net ID:- tbhatt22
=======================================================================

Python Version:- 3.7
IDE used:- PyCharm

========================================================================
Running Instructions:

Two arguments should be passed:- Path of Gold file, Path of Abstracts file

Example:- PageRank triparnabhattacharya$ python3 PageRank.py /Users/triparnabhattacharya/PycharmProjects/PageRank/gold /Users/triparnabhattacharya/PycharmProjects/PageRank/abstracts
=======================================================================

Functions Implemented:-

1. def preprocess_abstract_file(file_content, file):- Called for preprocessing each file from the abstract folder which ever file is matching with the gold and is passed one at a time. It extracts the words corresponding to the POS tags specified, performs stemming, removes stop-words. Used stop-words list provided in the assignment for removing stop-words from the corpus.

2. def create_vocab_graph(abstract_final1, file):-  This file checks the adjacency of the words based on their index, compares with the original file and add edges between them. 

3. def node_score(vocab_di, file):-  Calculates the node score for each node in the graph using the formula mentioned in the question.  The same scores are used for calculating bigram and trigram scores.

4. def find_top_ten_ngrams(di_node_score, file): -  Returns the top ngrams corresponding to the file passed. 

5. def find_exact_match(gold_final, file, top_ten_words):-  It compares the top ten ngrams of a particular file with the corresponding gold file and returns the index of the first matched word between gold and abstract.

6. def calculate_final_mrr(rank_list):-  Calculates the mar for top k words, where k ranges from 1 to 10.

7. def calculate_tf_idf():-  Calculates the tf-idf of each word based on the file. 


=========================================================================
Results:-


MRR of Top 1 word using Page Rank: 0.05639097744360909
MRR of Top 2 word using Page Rank: 0.08195488721804495
MRR of Top 3 word using Page Rank: 0.10300751879699238
MRR of Top 4 word using Page Rank: 0.12199248120300725
MRR of Top 5 word using Page Rank: 0.1388345864661651
MRR of Top 6 word using Page Rank: 0.14848370927318252
MRR of Top 7 word using Page Rank: 0.15331722162549177
MRR of Top 8 word using Page Rank: 0.15811045470819862
MRR of Top 9 word using Page Rank: 0.1618698532044394
MRR of Top 10 word using Page Rank: 0.16495255997135672

***********************Comparison ***************************

MRR of Top 1 word using TF-IDF: 0.07368421052631578
MRR of Top 2 word using TF-IDF: 0.10827067669172898
MRR of Top 3 word using TF-IDF: 0.13333333333333303
MRR of Top 4 word using TF-IDF: 0.1536340852130322
MRR of Top 5 word using TF-IDF: 0.16626566416040053
MRR of Top 6 word using TF-IDF: 0.17553884711779402
MRR of Top 7 word using TF-IDF: 0.1818761188685996
MRR of Top 8 word using TF-IDF: 0.18751521661296047
MRR of Top 9 word using TF-IDF: 0.1915252416756173
MRR of Top 10 word using TF-IDF: 0.1947583243823842

**********************Process Completed**********************
