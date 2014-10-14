# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 01:30:41 2014

@author: Meg McCauley

welcome.py
"""
import pygame as pyg
from pygame.locals import *

def main():
    
    # Writes window title text
    pyg.init()
    screen = pyg.display.set_mode((800, 800))   # screen is what is displayed
    pyg.display.set_caption('Spider Tic-Tac-Toe')
    
    # Create and draw background on Surface
    background = pyg.Surface(screen.get_size()) # background is a surface
    background = background.convert()
    background.fill((250, 250, 250))
    screen.blit(background, (0, 0))
    
    # Display title text
    font = pyg.font.Font("fonts/RobotoCondensed-Light.ttf", 36)
    text = font.render("Welcome to Spider Tic-Tac-Toe!", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    screen.blit(text, textpos)
    pyg.display.flip()

    # Sets up exiting via the red X or the ESC key
    while True:
        for event in pyg.event.get():
            if event.type == QUIT:
                pyg.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pyg.quit()
                    return
                    
if __name__ == '__main__':
    main()