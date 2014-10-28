# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:11:12 2014

@author: Meg McCauley
"""

import pygame as pyg
import welcome
from rules_text import rules_list

from pygame.locals import *

def rules_main():
    
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
    main_button = welcome.Button()
    main = main_button.create_button(background_image,(60,60,60), 0, 0, 150, 80, 0, "Main Menu",(255,255,255))
    main_pos = main.get_rect()
    main_pos.centerx = screen.get_rect().centerx        
    screen.blit(main,main_pos)
    pyg.display.flip()
    
    default_font = pyg.font.Font('fonts/RobotoCondensed-Light.ttf', 18) # Bring in the default font
    title_font = pyg.font.Font('fonts/RobotoCondensed-Light.ttf', 25)
    
    # Transparent Rectangle
    trans = pyg.Surface((600,600)) #starts at (0,0) and builds (width,height)
    trans.set_alpha(215) # 0 is invisible, 255 is solid, 128 is recommended
    trans.fill((60,60,60))
    screen.blit(trans,(100,150)) # refreshes the screen starting at (right,down)
    
    # For loop to wrap text from rules_text.py
    
    text_height = 100
    
    for i in range(len(rules_list)):
        if (rules_list[i][1]) == 0:     # Is this body text? Make the font and spacing smaller
            objective = default_font.render(rules_list[i][0], 1, (255, 255, 255))
            objective_pos = objective.get_rect()
            text_height += 30
            objective_pos.top = text_height
        else:   # Is this title text? Make the font and spacing bigger
            objective = title_font.render(rules_list[i][0], 1, (255, 255, 255))
            objective_pos = objective.get_rect()
            text_height += 45
            objective_pos.top = text_height
        objective_pos.left = 125    # Stay the same
        screen.blit(objective, objective_pos)   # Do every loop
    pyg.display.flip()

    # Add pictures to show straight rules
    straight = pyg.image.load("straight.png")
    straight = pyg.transform.scale(straight,(200, 200))
    pyg.display.set_icon(straight)
    screen.blit(straight,[100,550])
    pyg.display.flip()

    # Add pictures to show curve rules
    curve = pyg.image.load("curve.png")
    curve = pyg.transform.scale(curve,(200, 200))
    pyg.display.set_icon(curve)
    screen.blit(curve,[300,550])
    pyg.display.flip()

    # Add pictures to show spiral rules
    spiral = pyg.image.load("spiral.png")
    spiral = pyg.transform.scale(spiral,(200, 200))
    pyg.display.set_icon(spiral)
    screen.blit(spiral,[500,550])
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
                    welcome.welcome_main()
                    return

if __name__ == '__main__':
    from welcome import Button #Activates the button class    
    pyg.init()
    rules_main()