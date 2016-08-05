# -*- coding: utf-8 -*-
import json

def read_file(filename, select = 1):
  fp = open(filename, 'r')
  data = []
  for line in fp:
    if select == 0:
      line = line[line.find('.')+1 : ]  
    data.append(line)
  return data

"""
def unit_test_read_file():
  data = read_file('./dev_for_8')
  print len(data)
  print data[0]

def unit_test():
  unit_test_read_file()
"""

def process_and_save_data(word_prob_info_file, wp, tepmlate, equation):
  data_list = []
  for i in range(len(wp)):
    temp_dict = {}
    temp_dict["index"] = str(i+1)
    temp_dict["question"] = wp[i]
    temp_dict["template"] = template[i]
    temp_dict["equation"] = equation[i]
    data_list.append(temp_dict) 
  fp = open(word_prob_info_file, 'w')
  json.dump(data_list, fp, indent = 2)
  fp.close()
  print 'process and save json successfully!'

if __name__ == '__main__':
  wp = read_file('./dev_for_8', 0)
  template = read_file('./data_baidu_template')
  equation = read_file('./data_baidu_equation')
  process_and_save_data('./word_prob.json', wp, template, equation)
  
