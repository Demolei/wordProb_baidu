# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:50:17 2016

@author: demow
"""
from __future__ import division
from WordProbParser import *
from sympy.solvers import solve
from sympy import symbols
from math import log
from WordProbModel import *
from time import time
from Number import *
import EquationSolution
import re
import sys
import os

__metaclass__ = type
class WordProbFeature:
    permutations = {}


    @staticmethod
    def get_var_num(equ, start_var):
        n = 0
        while True:
            if equ.find(start_var) == -1:
                return n
            else:
                start_var = chr(ord(start_var)+1)
                n = n+1
    
    @staticmethod
    def get_solution(equation):
        equation = equation.strip(' ,')
        equation = equation.replace('= 0', '')
        m, n, k = symbols('m n k')
        equation = 'solve([' + equation + ']' + ',[m,n,k])'
        _result = eval(equation)
        result = []
        # print _result
        if _result:
            for value in _result.values():
                try:
                    result.append(float(value))
                except TypeError:
                    continue
        return result
        
    @staticmethod
    def permutate(data, n):
        if len(data) < n or n <= 0:
            return []

        permutations = []
        for index, item in enumerate(data):
            if n == 1:
                # yield [item]
                permutations.append([item])
            else:
                _data = data[:]
                del _data[index]
                for sub_seq in WordProbFeature.permutate(_data, n-1):
                    # yield [data[index]]+sub_seq
                    permutations.append([data[index]]+sub_seq)
        return permutations

    @staticmethod
    def is_correct_numerically(correct_ans_element, calculated_ans):
        for calculated_ans_element in calculated_ans:
            if calculated_ans_element == correct_ans_element:
                return True

        for calculated_ans_element in calculated_ans:
            if correct_ans_element == 0:
                if abs(calculated_ans_element) < 0.000001:
                    return True
            else:
                if abs(calculated_ans_element-correct_ans_element) < 0.000001:
                      return True
        else:
            return False


class WordProbSolutionInfo:
    def __init__(self, equ_template, equation, ans):
        self.equ_template = self.formulate_equ_template(equ_template)
        self.equation = self.formulate_equ_template(equation)
        try:
            self.ans = eval(ans)
        except TypeError:
            self.ans = ans
        self.sub_equs = self.get_sub_equation(equ_template)
        print self.equ_template, self.ans

    @staticmethod
    def formulate_equ_template(equ_template):
        equ_template = equ_template.strip()
        equ_template = equ_template.strip(' ,')
        return equ_template

    @staticmethod
    def get_sub_equation(equ_template):
        equ_template = WordProbSolutionInfo.formulate_equ_template(equ_template)
        sub_equs = []
        for sub_equ in equ_template.split(','):
            if sub_equ:
                sub_equs.append(sub_equ.strip())
        return sub_equs



def is_correct_template(prob, nums, template):
    n = WordProbFeature.get_var_num(template, 'a')

    correct_ans = prob['ans']
    permutations = WordProbFeature.permutate(nums, n)
    
    for permutation in permutations:
        calculated_ans = EquationSolution.calc_word_prob[template](*permutation)
        for ans in correct_ans:
            if not WordProbFeature.is_correct_numerically(ans, calculated_ans):
                break
        else:
            return True

    return False

def is_equvalent_template(probs, equ_num, template1, template2):
    num_pattern = r'[0-9]+\.?[0-9]*'
    # Template has special numbers. They will be different.
    if re.search(num_pattern, template1.replace('= 0', '')) or re.search(num_pattern, template2.replace('= 0', '')):
        return False

    for prob in probs:
        if not is_correct_template(prob, equ_num[prob['index']], template2):
            return False
    return True

def normalize_equation_template(raw_word_prob_file, word_prob_info_file):
    fp = open(raw_word_prob_file)
    word_prob_data = json.load(fp)
    word_prob_raw_groups = {}
    word_prob_groups = {}
    word_prob_equ_number = {}  #{u'1': [11.0, 19.0]}

    number_pattern = r'(-?[0-9]+\.?[0-9]*)'
    count = 1
    for word_prob in word_prob_data:
        equ = word_prob['equation']
        ans = WordProbFeature.get_solution(equ)
        word_prob['ans'] = ans
        
        template = word_prob['template']
        n = WordProbFeature.get_var_num(template, 'a')
        template_pattern = re.escape(template)
        for idx in range(n):
            template_pattern = template_pattern.replace(chr(ord('a')+idx), number_pattern)
            
        prob_index = word_prob['index']
        word_prob_equ_number[prob_index] = list(re.findall(template_pattern, equ)[0])
        for idx, num in enumerate(word_prob_equ_number[prob_index]):
            word_prob_equ_number[prob_index][idx] = float(word_prob_equ_number[prob_index][idx])
            
        del word_prob['template']
        word_prob_raw_groups.setdefault(template, [])
        word_prob_raw_groups[template].append(word_prob)
        print count
        count += 1
        
    templates = word_prob_raw_groups.keys()

    
    for index, template1 in enumerate(templates):
        probs = word_prob_raw_groups[template1] #probs belonged certain template
        equvalent_template = None
        for template2 in templates[index+1:]:
            if is_equvalent_template(probs, word_prob_equ_number, template1, template2):
                word_prob_raw_groups[template2].extend(word_prob_raw_groups[template1])
                equvalent_template = template2
                break

        if not equvalent_template:
            word_prob_groups[template1] = word_prob_raw_groups[template1]
        else:
            print template1, template2

    #fp = open(word_prob_info_file, 'w')
    #json.dump(word_prob_groups, fp, indent = 2)
    #fp.close()


def read_json_word_prob_info(parse_rlt_dir, word_prob_info_json_file):
    fp = open(word_prob_info_json_file)
    word_porb_infos = json.load(fp)
    equ_templates = word_porb_infos.keys()

    sol_infos = {}
    word_probs = {}
    indexes = []
    for equ_template, word_prob_subset in word_porb_infos.items():
        for word_prob in word_prob_subset:
            index = word_prob["index"]
            ans = word_prob["ans"]
            equation = word_prob["equation"]    
            sol_infos[index] = WordProbSolutionInfo(equ_template, equation, ans)


def get_train_and_test_samples_totally(parse_rlt_dir, word_prob_info_file, output_dir, semi_supervised):
    read_json_word_prob_info(parse_rlt_dir, word_prob_info_file)
                   
    

if __name__ == '__main__':
    t = time()
    raw_word_prob_file = "data/word_prob.json"
    word_prob_info_file = 'model/word_prob_info.json'
    normalize_equation_template(raw_word_prob_file, word_prob_info_file)
    
    test_case_file_template = './data/indexes-1-fold-%d.txt'
    parse_rlt_dir = './parses/'

    # Get all the training and test samples
    semi_supervised = False
    output_dir = "./result/word_prob_ftr/"
    word_prob_model_dir = "./model/model/"
    # output_dir = "./result/word_prob_ftr_n_a/"
    # word_prob_model_dir = "./model/model_n_a/"
    if semi_supervised:
        output_dir = "./result/word_prob_ftr_semi/"
        word_prob_model_dir = "./model/model_semi/"
    ngram_file = word_prob_model_dir+"ngram.txt"
    
    get_train_and_test_samples_totally(parse_rlt_dir, word_prob_info_file, output_dir, semi_supervised)
    
    print 'time is ' + str(time() - t)