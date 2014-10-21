# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 19:31:10 2014

@author: megsaysrawr

Testing importing images, making them transparent, and scaling them
"""
import pygame as pyg
from pygame.locals import *

pyg.init()
screen = pyg.display.set_mode((800,800))

background = pyg.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))
screen.blit(background, (0, 0))
    
red_bug = pyg.image.load('redbug.png')
coord = width,height = (50,50)
new_red_bug = pyg.transform.scale(red_bug, (coord))
screen.blit(new_red_bug,(0,0))
pyg.display.flip()

# Wanna make it transparent? We're working on it. Here's how.
trans_red_bug = pyg.Surface.convert_alpha(new_red_bug)
trans_red_bug.set_alpha(128)
screen.blit(trans_red_bug,(100,100))
pyg.display.flip()