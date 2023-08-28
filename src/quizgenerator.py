#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 14:44:18 2022

@author: sandro
---------------------
Quiz Generator

This class operates under general question form under Moodle Quiz using
Embadded Answer - Cloze https://docs.moodle.org/38/en/Embedded_Answers_(Cloze)_question_type

It generates different realizations of a question with some basic randomnes in
the inputs, to generate different answers.

Inputs:
    - category_path: category under which questions will be imported (test/2022)
    -question_ID: specific question ID as a sub category under category_path
    - question_form: is a question form with free input/output tags 
"""

import re

class QuizGenerator:
    def __init__(self, category_path,question_ID,question_form_path):
        
        self.category_path = category_path
        self.question_ID = question_ID
        self.question_form = question_form_path
        
        # question form tags
        self.input_tag = '{inp:'
        self.output_tag = '{out:'
        self.tag_end = '}'
        
        [question_form, tag_inp, tag_out] = self.parseQuestionForm(question_form_path)
        self.question_form = question_form
        self.tag_inp = tag_inp
        self.tag_out = tag_out
        
        print('Question form summary:')
        print('  ->  inputs found:', tag_inp)
        print('  -> outputs found:', tag_out)
        
        
# ***********************
# *** Public methods ****
# ***********************

    def generateQuiz(self, xml_file_name, p_inp, p_out, p_rand, footer=None):
        
        # Check size of inputs and outputs in form and data
        if (len(p_inp) != len(self.tag_inp)) or (len(p_out) != len(self.tag_out)):
            print('ERROR: size mismatch!')
            print('   -> form_inputs={:d}, data_inputs={:d}'.format(len(self.tag_inp), len(p_inp)))
            print('   -> form_outputs={:d}, data_outputs={:d}'.format(len(self.tag_out), len(p_out)))
            return
        
        questions = []
        nq = len(p_rand)
        for i in range(nq):
            q = self.replaceFormFields(p_inp, p_out, p_rand[i])
            questions.append(q)
        
        self.writeQuizXML(xml_file_name, questions)
        self.writeQuizPreviewForm(questions[0])
        
        print()
        print('Generator summary:')
        print('  -> generated {:d} different questions'.format(len(questions)))
        print('  -> Quiz is written in "{:s}" XML file'.format(xml_file_name))
        print('  -> Quiz is now ready for import in Moodle, mus use XML format!')
        
        

# ***********************
# *** Private methods ***
# ***********************

    # parsing question form for the number of input fields and number of output fields
    def parseQuestionForm(self,qf):
        
        p_inp = self.input_tag + '+\d' + self.tag_end
        p_out = self.output_tag + '+\d' + self.tag_end
    
        form = ''
        tag_inp = []
        tag_out = []
        
        file = open(qf, "r")
        for line in file:
            tv = re.findall(p_inp, line)
            for t in tv: tag_inp.append(t)
            
            tv = re.findall(p_out, line)
            for t in tv: tag_out.append(t)
            
            form += line
        
        file.close()
            
        return [form, tag_inp, tag_out]
    
    
    # replace input/output fields with values text in question form
    def replaceFormFields(self, p_inp, p_out, p_rand):
        
        form = self.question_form
        
        np = len(self.tag_inp)
        for i in range(np):
            str_f = self.generateInputTxt(p_inp[i], p_rand[0][i])
            form = re.sub(self.tag_inp[i], str_f, form)
                   
        np = len(self.tag_out)
        for i in range(np):
            str_f = self.generateOutputTxt(i+1,p_out[i], p_rand[1][i])
            form = re.sub(self.tag_out[i], str_f, form)
            
        return form
        
        
    
    # Input text form;
    # p_inp format [x, dx, u, name, format]
    # p_rand - random value
    def generateInputTxt(self, p_inp, p_rand):
        
        val = '{{{:s}}}'.format(':'+p_inp[4])
        val = val.format(p_rand)
        st = r'\( {:s} = {:s} \, \mathrm{{{:s}}} \)'.format(p_inp[3],val,p_inp[2])
        st = st.replace('\\', '\\\\') # for regular expressions double escape char
        # print('input form:', st)
        
        return st
        
        
    # Output text form;
    # idn - output number
    # p_out format [p, e, u, format, name, comment]
    # p_rand - random_value
    def generateOutputTxt(self, idn, p_out, p_rand):
        
        val = '{{{:s}}}:{{{:s}}}'.format(':'+p_out[3], ':'+p_out[3])
        val = val.format(p_rand,p_out[1])
        unit = r'\mathrm{{{:s}}}'.format(p_out[2])
        st = r'<td align="right">{:d}</td>'.format(idn)
        st += r'<td align="right">\({:s}\)</td>'.format(p_out[4])
        st += r'<td align="right">{{{:d}:NUMERICAL:={:s}#}}</td>'.format(p_out[0], val)
        st += r'<td align="left">\({:s}\)</td>'.format(unit)
        st += r'<td align="left">{:s}</td>'.format(p_out[5])
        st = st.replace('\\', '\\\\')
        # print('output form:', st)
        
        return st
        
    # Write Quiz in XML file
    def writeQuizXML(self, file_name, questions):
        
        fp = open(file_name, 'w')
        
        # write Quiz header
        fp.write(self.getQuizHeader())
        fp.write('\n')
        
        # write all question realizations
        nq = len(questions)
        for i in range(nq):
            fp.write(self.getQuestionHeader(i+1))
            
            lines = questions[i].splitlines()
            for l in lines:
                fp.write('\t\t\t\t')
                fp.write(l)
                fp.write('\n')
            
            fp.write(self.getQuestionFooter())
            fp.write('\n')
            
        # write Quiz footer
        fp.write(self.getQuizFooter())
        fp.close()
    
    
    # Sets quiz headers tag based on category path and question ID
    def getQuizHeader(self):
        
        cp = self.category_path + '/' + self.question_ID
        
        form = '<?xml version="1.0" encoding="UTF-8"?>' + '\n'
        form += '<quiz>' + '\n'
        form += '\t' + '<question type="category">' + '\n'
        form += '\t\t' + '<category>' + '\n'
        form += '\t\t\t' + '<text><![CDATA[$course$/' + cp + ']]></text>' + '\n'
        form += '\t\t' + '</category>' + '\n'
        form += '\t' + '</question>' + '\n'
        
        return form
        
    
    # Closes quiz xml tag
    def getQuizFooter(self):
        
        form = '</quiz>'
        return form
    
    
    # Sets question headers tag based on question ID
    def getQuestionHeader(self, id_n):
        
        form = '\t' + '<!-- question {:03d} -->'.format(id_n) + '\n'
        form += '\t' + '<question type="cloze">' + '\n'
        form += '\t' + '<name>' + '\n'
        form += '\t' + '<text><![CDATA[Vprašanje - {:03d}]]></text>'.format(id_n) + '\n'
        form += '\t' + '</name>' + '\n'
        form += '\t' + '<questiontext>' + '\n'
        form += '\t' + '<text><![CDATA[' + '\n'
        
        return form
    
        
    # Closes question xml tag
    def getQuestionFooter(self):
        
        form = '\t\t\t' + ']]></text>' + '\n'
        form += '\t\t' + '</questiontext>' + '\n'
        form += '\t\t' + '<shuffleanswers>0</shuffleanswers>' + '\n'
        form += '\t' + '</question>' + '\n'
        
        return form
    
    # Write a preview form to include in html
    def writeQuizPreviewForm(self, q):
        
        fp = open('realization_form.txt', 'w')
        
        # write Quiz
        lines = q.splitlines()
        for l in lines:
            fp.write(l)
            fp.write('\n')
        
        fp.close()
        
        
        
        