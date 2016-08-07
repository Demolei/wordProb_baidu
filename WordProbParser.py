# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:51:10 2016

@author: demow
"""

import xml.etree.ElementTree as ETree
import networkx as nx
import matplotlib.pyplot as plt
import re
import json
__metaclass__ = type

class WordProb:
    def __init__(self, file_dir, prob_idx):
        self.prob_idx = prob_idx
        self.tree = ETree.parse(file_dir+'question-'+prob_idx+".xml")
        self.sentences = []
        self.corefs = []
        
    
    

if __name__ == '__main__':
    file_dir = "./parses/"
    prob_idx = '1'
    wp = WordProb(file_dir, prob_idx)