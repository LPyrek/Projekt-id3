import numpy as np
import pandas as pd
import os
import sys
from graphviz import Digraph 



# Funkcja liczaca entropię
def entropia(table):
    y = table.iloc[:,-1]
    n = len(y)
    unique_konkluzje = np.unique(y)
    entropia = 0
    for konkluzja in unique_konkluzje:
        count = len(y[y == konkluzja])
        p = count / n
        entropia += -p * np.log2(p)
    return entropia

# Funkcja obliczająca informacje atrybutu
def informacja(table, atrybut):
    rows_atrybut_true = table.loc[(table == atrybut).any(axis=1)]  # tabela zawierajaca wiersze potwierdzajaca atrybut  
    rows_atrybut_false = table.loc[~(table == atrybut).any(axis=1)] # tabela zawierajace wiersze zaprzeczajaca atrybut
    
    i = entropia(table)
    i_plus = entropia(rows_atrybut_true) 
    i_minus = entropia(rows_atrybut_false)
    n = len(table)
    n_plus = len(rows_atrybut_true)
    n_minus = len(rows_atrybut_false)
    if n == 0:
        return 0
    return i - (n_plus/n * i_plus + n_minus/n * i_minus)

# Funkcja wyznaczająca atrybut z najwiekszym zyskiem informacyjnym
def max_informacja(table):
    dic = dict()
    for atrybut in np.unique(table.iloc[:,:-1]):
        dic[atrybut] = informacja(table, atrybut)   
        
    return max(dic, key=lambda k: dic[k])

# Funkcja sprawdzająca czy tabela zawiera jednakową konkluzje
def isConclusion(table):
    return True if len(np.unique(table.iloc[:,-1])) <= 1 else False

# Funkcja dzieląca tabele 
def podzial(table, atrybut):
    
    table_true = table.loc[(table == atrybut).any(axis=1)]  # tabela zawierajaca wiersze potwierdzajaca atrybut 
    table_false = table.loc[~(table == atrybut).any(axis=1)] # tabela zawierajace wiersze zaprzeczajaca atrybut
    
    
    return table_true, table_false


# rysowanie drzewa binarnego decyzyjnego 
def id3(table, parent_idx = None, tree = Digraph()):
    
    atrybut = max_informacja(table)
    
    # inicjalizacja pierwszego root node'a
    if parent_idx is None:
        parent_idx = "r"
        tree.node(parent_idx, str(table.columns[table.isin([max_informacja(table)]).any()][0]) + " = " + str(atrybut) + " ?")
    
    (table_true, table_false) = podzial(table, atrybut)
    
    child_true_idx = parent_idx + "T"
    chlid_false_idx = parent_idx + "F"

    # chlid node true
    if isConclusion(table_true):
        tree.node(child_true_idx, table_true.iloc[0,-1], color='red')
        tree.edge(parent_idx, child_true_idx, "tak")
    else:
        tree.node(child_true_idx, str(table_true.columns[table_true.isin([max_informacja(table_true)]).any()][0]) + " = " + str(max_informacja(table_true)) + " ?") # 
        tree.edge(parent_idx, child_true_idx, "tak")
        id3(table_true, child_true_idx)
        
    # child node false  
    if isConclusion(table_false):
        tree.node(chlid_false_idx, table_false.iloc[0,-1], color='red')
        tree.edge(parent_idx, chlid_false_idx, "nie")
    else:
        tree.node(chlid_false_idx, str(table_false.columns[table_false.isin([max_informacja(table_false)]).any()][0]) + " = " + str(max_informacja(table_false)) + " ?")
        tree.edge(parent_idx, chlid_false_idx, "nie")
        id3(table_false, chlid_false_idx) 
    return tree



# implementacja dla pliku dane.csv
os.chdir(sys.path[0])
path = os.getcwd() + "\dane.csv"
dane = pd.read_csv(path)
tree = id3(dane)
tree.render('BinarneDrzewoDecyzyjne',view = True)
