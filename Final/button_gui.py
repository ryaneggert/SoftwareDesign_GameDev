# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 16:09:27 2014

@author: abigail
"""


import pygame as pyg
import Buttons
from pygame.locals import *
import eztext
import sttt
import welcome
# initialize the pygame module
pyg.init()


class name_buttons(object):
    """ Creates player buttons
    """
    def __init__(self, num_players):
        self.num_players = num_players

    def display(self):
        """Creates a surface on screen"""
        self.screen = pyg.display.set_mode((800, 800))

    def update_display(self, num_players, buttons):
        """Sets the background image and generates the buttons"""
        background_image = pyg.image.load("spiderweb.jpg")
        background_image = pyg.transform.scale(background_image, (800, 800))
        pyg.display.set_icon(background_image)
        pyg.display.set_caption("Spyder Tic-Tac-Toe")
        self.screen.blit(background_image, [0, 0])

        # define buttons list
        backbutton = buttons[0]
        nextbutton = buttons[1]
        player1 = buttons[2]
        player2 = buttons[3]

        if num_players == 3:
            player3 = buttons[4]

        # create main buttons
        backbutton.create_button(
            self.screen, (255, 255, 255), 0, 0, 150, 80, 0, "Back", (0, 0, 0))
        nextbutton.create_button(
            self.screen, (255, 255, 255), 650, 720, 150, 80, 0, "Play",
            (0, 0, 0))
        # call function (surface, (R,G,B), x, y, length, height, width, text on
        # button, text color)

        # Using num_players creates appropriate number of text inputs fields
        total_height = num_players * 200

        # starts at (0,0) and builds (width,height)
        trans = pyg.Surface((800, 70))
        trans.set_alpha(245)
        # 0 is invisible, 255 is solid, 128 is recommended
        trans.fill((60, 60, 60))
        # refreshes the screen starting at (right,down)
        self.screen.blit(trans, (0, 100))
        font = pyg.font.Font("fonts/RobotoCondensed-Light.ttf", 30)
        # pyg.display.flip()

        # draws rectangles spaced equally apart
        for i in range(200, total_height, 150):
            pyg.draw.rect(
                self.screen, (255, 255, 255), (200, i, 400, 80), 0)

        player1.create_button(
                self.screen, (255, 255, 255), 200, 200, 100, 80, 0, "Player 1",
                (0, 0, 0))
        player2.create_button(
                self.screen, (255, 255, 255), 200, 350, 100, 80, 0, "Player 2",
                (0, 0, 0))

        if num_players == 3:
            player3.create_button(
            self.screen, (255, 255, 255), 200, 500, 100, 80, 0, "Player 3",
            (0, 0, 0))
            text = font.render("Click on Player 1, Player 2, Player 3 to" +
                " enter your names", 1, (255, 255, 255))

        else:
            text = font.render("Click on Player 1, Player 2 to enter" +
                " your names", 1, (255, 255, 255))

        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().centerx
        textpos.centery = 135
        self.screen.blit(text, textpos)
        # pyg.display.flip()


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

        events = pyg.event.get()

        for event in events:

            if event.type == pyg.QUIT:
                pyg.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                if backbutton.pressed(pyg.mouse.get_pos()):
                    print "Previous page!"
                    welcome.welcome_main()
                    return
                elif nextbutton.pressed(pyg.mouse.get_pos()):
                    print "Play game!!!"
                    names = [txtbx.value, txtbx2.value]
                    if num_players == 3:
                        names.append(txtbx3.value)
                    sttt.stttmain(names)
                    return

                elif player1.pressed(pyg.mouse.get_pos()):
                    leave = 1
                    # print leave
                    # self.write()
                    break
                elif player2.pressed(pyg.mouse.get_pos()):
                    leave = 2
                    break
                elif num_players == 3:
                    if player3.pressed(pyg.mouse.get_pos()):
                        leave = 3
                    break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pyg.quit()
                    return

        if leave == 1:
            txtbx.update(events)
            txtbx.draw(viewname.screen)
            txtbx2.draw(viewname.screen)
            # print txtbx.value

        elif leave == 2:
            txtbx2.update(events)
            txtbx.draw(viewname.screen)
            txtbx2.draw(viewname.screen)
            # print txtbx2.value

        elif leave == 3:
            txtbx3.update(events)
            txtbx.draw(viewname.screen)
            txtbx2.draw(viewname.screen)

        buttons = [backbutton, nextbutton, player1, player2]

        if num_players == 3:
            txtbx3.draw(viewname.screen)
            buttons.append(player3)

        pyg.display.flip()
        viewname.update_display(num_players, buttons)

# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    num_players = 2
    main(num_players)
