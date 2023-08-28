#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 14:44:18 2022

@author: sandro
"""

# Nalaganje potrebnih paketoc
import sys

# sources path
sys.path.append('../src')

import random as rnd
import quizgenerator as qg

# ***********************
# *** Tools functions ***
# ***********************

# Generate random number
# y = x + rand(dx)
# rand(dx) is in the interval [-dx,dx]
def randValue(x,dx,N):
    
    return x + (2*rnd.randint(0,N) - N)/N * dx

# Returns question random values for inputs and for results
def getQuestionRandomValues(p_inp, nq):
    
    res = []
    for i in range(nq):
        y = modelFunction(p_inp)
        res.append(y)
        
    return res

# *******************************
# *** Quiz specific functions ***
# *******************************

# Model function based on input definitions
# - generate random inputs
# - generate results based on random inputs
def modelFunction(p_inp):
    N = 10000
    x = []
    
    # generate random numbers for inputs x
    for p in p_inp:
        v = randValue(p[0],p[1],N)
        x.append(v)
    
    # *** random inputs ***
    D0 = x[0]  # inital displacement
    Tf0 = x[1] # initial draft forward
    Ta0 = x[2] # initial draft afterward
    TPC = x[3] # TPC 
    m = x[4]   # discharged cargo mass (negative sign)
    rand_inp = [D0,Tf0,Ta0,TPC,m]
    
    # *** results ***
    Ts0 = (Tf0 + Ta0)/2 # initial mean draft
    dTs =  -m / TPC     # draft change
    D1 = D0 - m         # new displacement
    Ts1 = Ts0 + dTs/100 # new mean draft
    rand_res = [Ts0,dTs,D1,Ts1]
    
    return [rand_inp, rand_res]

# generates input parameters
def getInputParameters():
    # *** define inputs ***
    #
    # [x, dx, u, name, format]:
    #  x: mean,
    #  dx: random interval
    #  u: unit
    #  name: input variable name (possible use LaTeX form, i.e. \Delta)
    #  format: specify output format, based on formatted strings
    #
    # random value is calculated with function randValue(x,dx)
    
    D = [60000, 5000, 't',r'\Delta','.1f']          # displacement
    Tf = [10.5, 0.5, 'm',r'T_\mathrm{f}','.2f']     # draft forward
    Ta = [9.5, 0.5, 'm',r'T_\mathrm{a}','.2f']      # draft aft       
    TPC = [20.0, 2.0, 't/cm',r'\mathrm{TPC}','.2f'] # tone per centimeter - TPC
    m = [1000.0, 200.0, 't',r'\mathrm{m}','.2f']    # mass
    
    return [D, Tf, Ta, TPC, m]

# generate output parameters
def getOutputParameters():
    # *** define outputs properties ***
    #
    # [p, e, u, format, name, comment]:
    #  p: number of points for correct answer (must be integer)
    #  e: abslute error
    #  u: unit
    #  format: specify output format, based on formatted strings
    #  name: output variable name (possible use LaTeX form, i.e. \Delta)
    #  comment: comments related to result (description, points, ...)
    #
    # This are results of the Quiz!
    
    Ts0 = [1,0.02,'m','.2f',r'T_\mathrm{s}','začetni srednji ugrez; 1 točka']
    dTs = [2,2,'cm','.2f', r'\Delta T','sprememba ugreza; 2 točki']
    D1 = [1,5,'t','.1f',r'\Delta','deplasman na koncu; 1 točka']     
    Ts1 = [1,0.02,'m','.2f',r'T_\mathrm{s}','srednji ugrez na koncu; 2 točki']
    
    return [Ts0,dTs,D1,Ts1]

# ********************************
# *** Main part of the program ***
# ********************************
def main():
    
    # input parameters
    p_inp = getInputParameters()
    
    # output parameters
    p_out = getOutputParameters()
    
    # questions random values ([inputs, results]) 
    Nq = 10 # number of question random realizations
    p_rand = getQuestionRandomValues(p_inp, Nq) # random results


    # *** quiz parameters ***
    category_path = 'test/2022'
    question_ID = 'q-01'
    question_form_path = '../examples/quiz_form_01.txt'
    
    # *** initial Quiz ***
    quiz = qg.QuizGenerator(category_path, question_ID, question_form_path)
    # generate randomized Quiz
    quiz.generateQuiz(p_inp, p_out, p_rand)

if __name__ == '__main__':
    sys.exit(main())



