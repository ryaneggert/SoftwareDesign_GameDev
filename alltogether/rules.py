# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:11:12 2014

@author: Meg McCauley
"""

"""
Spyder Tic-Tac-Toe

Objective: Get four of your color bugs in a row to win. There are three ways to do this.
1. Straight
Place one bug in the center ring and three more in the same column up to the outer ring.
2. Curve
Place one bug anywhere and place three more in the same level ring.
3. Spiral
The most complex (and sneaky) way to win. One bug must be in the center ring. From here, place
your next three bugs up and over one, in either direction, until you reach the outer ring.
"""
import pygame as pyg
import welcome
from welcome import Button #Activates the button class
from pygame.locals import *

def main():
    
    pyg.init()
    pyg.font.init()
    screen = pyg.display.set_mode((800, 800))   # screen is what is displayed
    #pyg.display.set_caption('Spyder Tic-Tac-Toe Rules')
    
    # Add Spider Web background
    background_image = pyg.image.load("spiderweb.jpg")
    background_image = pyg.transform.scale(background_image,(800, 800))
    pyg.display.set_icon(background_image)
    pyg.display.set_caption("Spyder Tic-Tac-Toe Rules")
    screen.blit(background_image,[0,0])
    pyg.display.flip()
    
    # Create the main menu button
    main_button = Button()
    main = main_button.create_button(background_image,(255,255,255), 0, 0, 150, 80, 0, "Main Menu",(0, 0, 0))
    main_pos = main.get_rect()
    main_pos.centerx = screen.get_rect().centerx        
    screen.blit(main,main_pos)
    pyg.display.flip()
    
    # Checking for events (quitting, pressing buttons, etc.)
    while True:
        for event in pyg.event.get():
            if event.type == QUIT:
                pyg.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pyg.quit()
                    return
            elif event.type == MOUSEBUTTONDOWN:
                print 'mousedown'
                mouse_pos = pyg.mouse.get_pos()
                if main_button.pressed(mouse_pos):
                    print "Main Menu"
                    welcome.main()
                    return

main()