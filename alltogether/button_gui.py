# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 16:09:27 2014

@author: abigail
"""


import pygame, Buttons, string, welcome

# initialize the pygame module
pygame.init()
from pygame.locals import *

class new_button:
       
    def __init__(self):
        self.main()
    
    #Create a display
    def display(self):
        # create a surface on screen that has the size of 800 x 800
        self.screen = pygame.display.set_mode((800,800))

    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
              return event.key
            else:
              pass
    def display_box(self, screen, message):
      fontobject = pygame.font.Font(None,30)
      if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (0,0,0)),
                    (200, 240))
      pygame.display.flip()
      
    def ask(self, screen, question):
        pygame.font.init()
        current_string = []
        self.display_box(self.screen, question + ": " + string.join(current_string,""))
        while 1:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            inkey = self.get_key()
            if inkey == K_BACKSPACE:
                pygame.draw.rect(self.screen, (255,255,255), (200, 240, 400, 80), 0)
                current_string = current_string[0:-1]
            elif inkey == K_ESCAPE:
                pygame.quit()
                return
            elif inkey == K_RETURN:
                break
            elif inkey == K_MINUS:
                current_string.append("_")
            elif inkey <= 127:
                current_string.append(chr(inkey))

            self.display_box(self.screen, question + ": " + string.join(current_string,""))
        return string.join(current_string,"")
        #print new_button.ask(self.screen, "Player 1 Name") + " was entered"
        pygame.display.flip()

      
    def update_display(self):
        # load the image
        background_image = pygame.image.load("spiderweb.jpg")
        background_image = pygame.transform.scale(background_image,(800, 800))
        pygame.display.set_icon(background_image)
        pygame.display.set_caption("minimal program")
        self.screen.blit(background_image,[0,0])
        # draw a rectangle (x,y,length,height) where upper left corner position = x,y and extends to the right (width,height)
        #pygame.draw.rect(screen, (255,255,255), (0, 0, 150, 80), 0)
        #pygame.draw.rect(screen, (255,255,255),(650, 720, 150,80), 0)
        self.backbutton.create_button(self.screen,(255,255,255), 0, 0, 150, 80, 0, "Back",(0, 0, 0))
        self.nextbutton.create_button(self.screen,(255,255,255), 650, 720, 150, 80, 0, "Play",(0, 0, 0))
        #               call function (surface, (R,G,B), x, y, length, height, width, text on button, text color)
        
        pygame.draw.rect(self.screen, (255,255,255), (200, 240, 400, 80), 0)
        pygame.draw.rect(self.screen, (255,255,255), (200, 480, 400, 80), 0)
        pygame.display.flip() 
        
    # define a variable to control the main loop
    def main(self):
        self.backbutton = Buttons.Button()
        self.nextbutton = Buttons.Button()
        self.display()

        while True:
            self.update_display()
            # print self.ask(self.screen, "Player 1 Name")
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    if self.backbutton.pressed(pygame.mouse.get_pos()):
                        print "Previous page!"
                        welcome.main()
                    elif self.nextbutton.pressed(pygame.mouse.get_pos()):
                        print "Play game!!!"
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        return

# run the main function only if this module is executed as the main script
if __name__=="__main__":
    # call the main function
    obj = new_button()
    #main()