# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 01:30:41 2014

@author: Meg McCauley

welcome.py
Sourced from Ryan Eggert's pygametest1.py
"""
import pygame as pyg
from pygame.locals import *

"""Button class sourced from Simon H. Larsen, http://lagusan.com/button-drawer-python-2-6/"""

class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pyg.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myFont = pyg.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):           
        for i in range(1,10):
            s = pyg.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pyg.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pyg.draw.rect(surface, color, (x,y,length,height), 0)
        pyg.draw.rect(surface, (190,190,190), (x,y,length,height), 1)  
        return surface
    
    #Edited from original to shorten (one if statement with ands, not four)
    def pressed(self, mouse_pos):
        if mouse_pos[0] > self.rect.topleft[0] and mouse_pos[1] > self.rect.topleft[1] and mouse_pos[0] < self.rect.bottomright[0] and mouse_pos[1] < self.rect.bottomright[1]:
            # print "Some button was pressed!"
            return True
        else: return False

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
    
     # Make a blue 2 player button
    p2_button = Button()
    p2 = p2_button.create_button(background,(0,0,255), 200, 200, 400, 75, 0, "2 Players", (0,0,0))
    p2pos = p2.get_rect()
    p2pos.centerx = screen.get_rect().centerx   
    screen.blit(p2, p2pos)
    pyg.display.flip()
    
     # Make a red 3 player button
    p3_button = Button()
    p3 = p3_button.create_button(background,(255,0,0), 200, 400, 400, 75, 0, "3 Players", (0,0,0))
    p3pos = p3.get_rect()
    p3pos.centerx = screen.get_rect().centerx   
    screen.blit(p3, p3pos)
    pyg.display.flip()
    
    # Make a purple rules button
    rules_button = Button()
    rule = rules_button.create_button(background,(157,20,181), 200, 600, 400, 75, 0, "Rules", (0,0,0))
    rulespos = rule.get_rect()
    rulespos.centerx = screen.get_rect().centerx   
    screen.blit(rule, rulespos)
    pyg.display.flip()
    
    # Display title text
    font = pyg.font.Font("fonts/RobotoCondensed-Light.ttf", 54)
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
            elif event.type == MOUSEBUTTONDOWN: # Only register click on mouse button down.
                print 'mousedown'
                mouse_pos = pyg.mouse.get_pos()
                if rules_button.pressed(mouse_pos):
                    print 'Rules'
                if p2_button.pressed(mouse_pos):
                    print '2 Players'
                if p3_button.pressed(mouse_pos):
                    print '3 Players'
                    
if __name__ == '__main__':
    main()