# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 16:09:27 2014

@author: abigail
"""


import pygame
import Buttons  # , string, welcome
from pygame.locals import *
import eztext
import sttt
import welcome
# initialize the pygame module
pygame.init()


class name_buttons(object):

    def __init__(self, num_players):
        self.num_players = num_players
        
    # Create a display
    def display(self):
        # create a surface on screen that has the size of 800 x 800
        self.screen = pygame.display.set_mode((800, 800))

    def update_display(self, num_players, buttons):
        # load the image
        background_image = pygame.image.load("spiderweb.jpg")
        background_image = pygame.transform.scale(background_image, (800, 800))
        pygame.display.set_icon(background_image)
        pygame.display.set_caption("Spyder Tic-Tac-Toe")
        self.screen.blit(background_image, [0, 0])
        # draw a rectangle (x,y,length,height) where upper left corner position = x,y and extends to the right (width,height)
        #pygame.draw.rect(screen, (255,255,255), (0, 0, 150, 80), 0)
        #pygame.draw.rect(screen, (255,255,255),(650, 720, 150,80), 0)
        backbutton = buttons[0]
        nextbutton = buttons[1]
        player1 = buttons[2]
        player2 = buttons[3]
        if num_players == 3:
            player3 = buttons[4]

        backbutton.create_button(
            self.screen, (255, 255, 255), 0, 0, 150, 80, 0, "Back", (0, 0, 0))
        nextbutton.create_button(
            self.screen, (255, 255, 255), 650, 720, 150, 80, 0, "Play", (0, 0, 0))
        # call function (surface, (R,G,B), x, y, length, height, width, text on
        # button, text color)

        # Using num_players creates appropriate number of text inputs fields
        total_height = num_players * 200

        for i in range(200, total_height, 150):
            pygame.draw.rect(
                self.screen, (255, 255, 255), (200, i, 400, 80), 0)

        if num_players == 3:
            player1.create_button(
                self.screen, (255, 255, 255), 200, 200, 100, 80, 0, "Player 1", (0, 0, 0))
            player2.create_button(
                self.screen, (255, 255, 255), 200, 350, 100, 80, 0, "Player 2", (0, 0, 0))
            player3.create_button(
                self.screen, (255, 255, 255), 200, 500, 100, 80, 0, "Player 3", (0, 0, 0))

        else:
            player1.create_button(
                self.screen, (255, 255, 255), 200, 200, 100, 80, 0, "Player 1", (0, 0, 0))
            player2.create_button(
                self.screen, (255, 255, 255), 200, 350, 100, 80, 0, "Player 2", (0, 0, 0))
        # pygame.display.flip()

    # define a variable to control the main loop
def main(num_players):
    backbutton = Buttons.Button()
    nextbutton = Buttons.Button()
    player1 = Buttons.Button()
    player2 = Buttons.Button()
    player3 = Buttons.Button()
    viewname = name_buttons(num_players)
    viewname.display()
    txtbx = eztext.Input(x=350, y=225, maxlength=15, color=(0, 0, 0))
    txtbx2 = eztext.Input(x=350, y=375, maxlength=15, color=(0, 0, 0))
    if num_players == 3:
        txtbx3 = eztext.Input(x=350, y=525, maxlength=15, color=(0, 0, 0))
    leave = 0
    while True:

        # print self.ask(self.screen, "Player 1 Name")

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                if backbutton.pressed(pygame.mouse.get_pos()):
                    print "Previous page!"
                    welcome.welcome_main()
                    return
                elif nextbutton.pressed(pygame.mouse.get_pos()):
                    print "Play game!!!"
                    names = [txtbx.value, txtbx2.value]
                    if num_players == 3:
                        names.append(txtbx3.value)
                    sttt.stttmain(names)
                    return

                elif player1.pressed(pygame.mouse.get_pos()):
                    leave = 1
                    # print leave
                    # self.write()
                    break
                elif player2.pressed(pygame.mouse.get_pos()):
                    leave = 2
                    break
                elif num_players == 3:
                    if player3.pressed(pygame.mouse.get_pos()):
                        leave = 3
                    break   

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return

        if leave == 1:
            # self.update_display()
            txtbx.update(events)
            txtbx.draw(viewname.screen)
            txtbx2.draw(viewname.screen)
                            # print txtbx.value
        elif leave == 2:
            # self.update_display()
            txtbx2.update(events)
            txtbx.draw(viewname.screen)
            txtbx2.draw(viewname.screen)

            # print txtbx.value
        elif leave == 3:
            txtbx3.update(events)
            txtbx.draw(viewname.screen)
            txtbx2.draw(viewname.screen)

        buttons = [backbutton, nextbutton, player1, player2]
        if num_players == 3:
            txtbx3.draw(viewname.screen)
            buttons.append(player3)
        pygame.display.flip()
        viewname.update_display(num_players,buttons)

# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    num_players = 3
    main(num_players)
