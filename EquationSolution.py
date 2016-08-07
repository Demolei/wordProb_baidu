# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:51:31 2016

@author: demow
"""

from __future__ import division

# ax = b
def linear_equation_v1o1(a,b):
    if a == 0:
        return []
    else:
        return [b/a]
# a1x+b1y=c1
# a2x+b2y=c2
def linear_equation_v2o1(a1, b1, c1, a2, b2, c2):

    t1 = a1*b2 - b1*a2
    if t1 == 0:
        return []

    t2 = c1*b2 - b1*c2
    t3 = a1*c2 - c1*a2

    return t2/t1, t3/t1

def three_determinant(a1,b1,c1,a2,b2,c2,a3,b3,c3):
    return a1*b2*c3 + b1*c2*a3 + c1*a2*b3 - a3*b2*c1 - b3*c2*a1 - c3*a2*b1

def linear_equation_v3o1(a1,b1,c1,d1,a2,b2,c2,d2,a3,b3,c3,d3):
    t1 = three_determinant(a1,b1,c1,a2,b2,c2,a3,b3,c3)
    t2 = three_determinant(d1,b1,c1,d2,b2,c2,d3,b3,c3)
    t3 = three_determinant(a1,d1,c1,a2,d2,c2,a3,d3,c3)
    t4 = three_determinant(a1,b1,d1,a2,b2,d2,a3,b3,d3)
    
    if t1 == 0:
        return []
    
    return t2/t1, t3/t1, t4/t1

calc_word_prob = {}
calc_word_prob['-k+-m+n = 0, -a+m = 0, -b+n = 0'] = lambda a, b: linear_equation_v3o1(-1,1,-1,0,1,0,0,a,0,1,0,b)
calc_word_prob['-a+b+-c+m = 0'] = lambda a,b,c: linear_equation_v1o1(1, a+c-b)
calc_word_prob['a+b+-c+m = 0'] = lambda a,b,c: linear_equation_v1o1(1, c-b-a)
calc_word_prob['-a+b+m = 0'] = lambda a,b: linear_equation_v1o1(1, a-b)
calc_word_prob['-k+m+n = 0, a+-m+n = 0, -b+m = 0'] = lambda a,b: linear_equation_v3o1(1,1,-1,0,-1,1,0,-a,1,0,0,b)
calc_word_prob['a+-m+n = 0, -b+-c+m = 0'] = lambda a,b,c:linear_equation_v2o1(-1,1,-a,1,0,b+c)
calc_word_prob['a+-k-m+n = 0, -b+m = 0, -c+k = 0'] = lambda a,b,c: linear_equation_v3o1(-1,1,-1,-a,1,0,0,b,0,0,1,c)
calc_word_prob['-a+-m+n = 0, -b+m = 0'] = lambda a,b: linear_equation_v2o1(-1,1,a,1,0,b)
calc_word_prob['-a+-m+n = 0, -b+-k+m = 0, -c+k = 0'] = lambda a,b,c: linear_equation_v3o1(-1,1,0,a,1,0,-1,b,0,0,1,c)
calc_word_prob['a+-b+-c+m = 0'] = lambda a,b,c: linear_equation_v1o1(1,b+c-a)
calc_word_prob['k+-m+n = 0, -a+m = 0, -b+n = 0'] = lambda a,b: linear_equation_v3o1(-1,1,1,0,1,0,0,a,0,1,0,b)
calc_word_prob['a+-m+n = 0, -b+m = 0'] = lambda a,b: linear_equation_v2o1(-1,1,-a,1,0,b)
calc_word_prob['-a+-b+m = 0'] = lambda a,b: linear_equation_v1o1(1, a+b)
calc_word_prob['-a+-m+n = 0, b+-k+m = 0, -c+k = 0'] = lambda a,b,c: linear_equation_v3o1(-1,1,0,a,1,0,-1,-b,0,0,1,c)
calc_word_prob['a+-m+n = 0, b+-k+m = 0, -c+k = 0'] = lambda a,b,c: linear_equation_v3o1(-1,1,0,-a,1,0,-1,-b,0,0,1,c)
calc_word_prob['a+a+-b+m = 0'] = lambda a,b: linear_equation_v1o1(1,b-a-a)
calc_word_prob['a+-m+n = 0, -b+-k+m = 0, -c+k = 0'] = lambda a,b,c: linear_equation_v3o1(-1,1,0,-a,1,0,-1,b,0,0,1,c)
calc_word_prob['-a+b+c+-d+m = 0'] = lambda a,b,c,d: linear_equation_v1o1(1,d+a-b-c)
    
if __name__ == '__main__':
    print linear_equation_v2o1(3, 2, 6, 6, 4, 12)
    print linear_equation_v2o1(3, -5, 0, 1, 1, 24)
    print calc_word_prob['(a*m)+(b*n)+-c = 0, (-d*m)+n = 0'](*[1, 1, 177, 2])
    print calc_word_prob['(a*m)+(b*n)+-c = 0, (d*n)+(b*m)+-e = 0'](*[4, 2, 1, 3, 0.7])