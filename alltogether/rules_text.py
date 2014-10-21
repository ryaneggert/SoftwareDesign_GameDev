# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 21:36:40 2014

@author: Meg McCauley

This file is designed to keep track of the rules text in a non-obtrusive way.
It will be imported into rules.py and looped through in order to create a
very low power word wrap.

A list composed of tuples where the first element is the text
and the second element indicates 0 or 1 for default_font or title_font
"""

rules_list = [('Objective',1),
              ('Get four of the bugs (of your color) in a row to win. There are three ways to do this.',0),
              ('1. Straight',1),
              ('Place one bug in the center ring and three more in the same column up to the',0),
              ('outer ring.',0),
              ('2. Curve',1),
              ('Place one bug anywhere and place three more in the same level ring.',0),
              ('3. Sprial',1),
              ('The most complex (and sneaky) way to win. One bug must be in the center ring',0),
              ('From here, place your next three bugs up and over one cell, in either direction',0),
              ('until you reach the outer ring',0)]
