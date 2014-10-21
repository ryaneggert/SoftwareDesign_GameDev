# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 20:37:28 2014

@author: Meg McCauley

Given the cartesian center of a sector (sectorcenter) of a gameboard, draws a semitransparent icon over that sector (for hovering)

If statement: If this is player1, make it red, player2, make it blue

NEED: blue bug, purple bug (for now, use different images)
Ability to make transparent bugs (being worked on in image)
"""
import pygame as pyg
from pygame.locals import *

def main():
    pyg.init()
    screen = pyg.display.set_mode((800,800))
    place_bug(screen,1)

def drawhovericon(sectorcenter): #also eventually intake (player)
    pass
#    if player == 1:
#        image = red_bug
#    elif player == 2:
#        image = blue_bug
#    else player == 3:
#        image = purple_bug
    
def place_bug(screen,player):
    if player == 1:
        image = pyg.image.load('redbug.png')
    elif player == 2:
        image = pyg.image.load('bluebug.png')
    elif player == 3:
        image = pyg.image.load('purplebug.png')
    screen.fill((50,100,100))
    rect = image.get_rect()
    rect_coord = rect_x, rect_y = (rect.centerx, rect.centery)
    coord = width,height = (50,50)
    new_image = pyg.transform.scale(image, (coord))
    screen.blit(new_image,(rect_coord))
    pyg.display.flip()
    
main()