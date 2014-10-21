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

# Wanna make it transparent? We're working on it. Here's how you do it with rectangles.

#trans = pyg.Surface((600,600)) #starts at (0,0) and builds (width,height)
#trans.set_alpha(215) # 0 is invisible, 255 is solid, 128 is recommended
#trans.fill((60,60,60))
#screen.blit(trans,(100,150)) # refreshes the screen starting at (right,down)