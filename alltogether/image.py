# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 19:31:10 2014

@author: megsaysrawr

Testing importing images, making them transparent, and scaling them
"""
import pygame as pyg
from pygame.locals import *

running = 1

pyg.init()
screen = pyg.display.set_mode((800,800))
screen_img = pyg.Surface((660,660),SRCALPHA)


red_bug = pyg.image.load('redbug.png').convert_alpha()
blue_bug = pyg.image.load('bluebug.png')

background = pyg.Surface(screen.get_size())
background = background.convert()
background.fill((100, 100, 100))
screen.blit(background, (0, 0))
    
coord = width,height = (50,50)
new_red_bug = pyg.transform.scale(red_bug, (coord))
trans_blue_bug = pyg.Surface.convert_alpha(blue_bug)
trans_blue_bug.set_alpha(215)

while running:
    screen.blit(new_red_bug,(0,0))
    screen.blit(trans_blue_bug,(100,100))
    pyg.display.flip()