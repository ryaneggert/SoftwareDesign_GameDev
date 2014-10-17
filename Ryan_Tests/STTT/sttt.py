## sttt.py ##
# MVC architecture for spider tic-tac-toe

import pygame as pyg
import math, itertools
from pygame.locals import *

class GameModel(object):
    """docstring for GameModel"""
    def __init__(self):
        super(GameModel, self).__init__()
        
    def mouseposition(self):
        pass

class GameView(object):
    """docstring for GameView"""
    def __init__(self):
        super(GameView, self).__init__()

class GameController(object):
    """Read events. Send inputs to GameModel object"""

    def __init__(self):
        super(GameController, self).__init__()

    def exitevents(self):
        """Checks for exit events"""
        quit = 0
        for event in self.currentEvents:
            if event.type == QUIT:
                quit = 1
            elif event.type == KEYDOWN:
                if event.key == K_h:
                    quit = 1
        self.quit = quit
        return quit

    def keyboardevents(self):
        """Checks for keyboard input"""
        keyInput = None
        for event in self.currentEvents:
            if event.type == KEYDOWN and event.key != K_ESCAPE:
                keyInput = event.key
        self.keyInput = keyInput
        return keyInput

    def mouseevents(self):
        """Handles mouse events (clicks and position)"""
        click = None
        mousePos = None
        for event in self.currentEvents:
            if event.type == MOUSEMOTION:   # Only update when mouse moves
                mousePos = mX,mY = pyg.mouse.get_pos()     # Current position of mouse cursor 
            elif event.type == MOUSEBUTTONDOWN: # Only register click on mouse button down.
                leftClick = pyg.mouse.get_pressed()[0] # Status of left mouse button
                if leftClick == 1:
                    click = 'Left'
        return mousePos,click

    def mousecarttopolar(self):
        mX,mY = mouseLoc
        cX,cY = webCenter
        rmX = (mX-cX)   # Remapped x (x if the web center is defined now to be the origin)
        rmY = -(mY-cY)   # Remapped y (y if the web center is defined now to be the origin)
        mr = math.hypot(rmX, rmY)
        mtheta = math.degrees(math.atan2(rmY,rmX))
        if mtheta < 0:
            mtheta += 360
        return mr, mtheta

    # def getevents(self, currentEvents):
    #     for event in pyg.event.get():
    #         if event.type == QUIT:
    #             # pyg.quit()
    #             return
    #         elif event.type == KEYDOWN:
    #             if event.key == K_ESCAPE:
    #                 # pyg.quit()
    #                 return
    #         elif event.type == MOUSEMOTION:     # Only update when mouse moves

    #             mousePos = mX,mY = pyg.mouse.get_pos()     # Current position of mouse cursor
    #             mousePol = mousetopolar(mousePos, spiderweb.centerpoint)
    #             del sectorHist [0]
    #             sectorHist.append(spiderweb.getmousesector(mousePol))
    #             # spiderweb.getmouseregion(mousePos)  # Draw dots following the cursor
    #         elif event.type == MOUSEBUTTONDOWN: # Only register click on mouse button down.
    #             lClick = pyg.mouse.get_pressed()[0] # Status of left mouse button
    #             if lClick == 1:
    #                 print 'Left Click'
    #                 player +=1


        
        
        





def stttmain():
    pyg.init()
    pyg.event.get()

    TTTControl = GameController()
    TTTView = GameView()
    TTTModel = GameModel()

    while True:
        TTTControl.currentEvents = pyg.event.get()
        quit = TTTControl.exitevents()
        keys = TTTControl.keyboardevents()
        mousepos, mouseclick = TTTControl.mouseevents()
        print mousepos





if __name__ == '__main__':
    stttmain()