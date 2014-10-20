## sttt.py ##
# MVC architecture for spider tic-tac-toe

import pygame as pyg
import math, itertools
from pygame.locals import *


class GameController(object):
    """Read events. Send inputs to GameModel object"""

    def __init__(self):
        super(GameController, self).__init__()

    def exitevents(self):
        """Checks for exit events"""
        quit = 0
        for event in self.currentevents:
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
        for event in self.currentevents:
            if event.type == KEYDOWN and event.key != K_ESCAPE:
                keyInput = event.key
        self.keyinput = keyInput
        return keyInput

    def mouseevents(self, GameBoard):
        """Handles mouse events (clicks and position)"""
        click = None
        mousePos = None
        for event in self.currentevents:
            if event.type == MOUSEMOTION:   # Only update when mouse moves
                mousePos = mX,mY = pyg.mouse.get_pos()     # Current position of mouse cursor
                mousePolPos = self.mousecarttopolar(mousePos, GameBoard.centerpoint)
            elif event.type == MOUSEBUTTONDOWN: # Only register click on mouse button down.
                leftClick = pyg.mouse.get_pressed()[0] # Status of left mouse button
                if leftClick == 1:
                    click = 'Left'
        self.mousepolpos = (mousePolPos)
        return mousePos, mousePolPos,click

    def mousecarttopolar(self, mouseLoc, webCenter):
        mX,mY = mouseLoc
        cX,cY = webCenter
        rmX = (mX-cX)   # Remapped x (x if the web center is defined now to be the origin)
        rmY = -(mY-cY)   # Remapped y (y if the web center is defined now to be the origin)
        mr = math.hypot(rmX, rmY)
        mtheta = math.degrees(math.atan2(rmY,rmX))
        if mtheta < 0:
            mtheta += 360
        mousePolPos = (mr, mtheta)
        return mousePolPos


class GameModel(object):
    """docstring for GameModel"""
    def __init__(self, centerPoint, radiusIncrement):
        super(GameModel, self).__init__()
        self.centerpoint = self.webCX, self.webCY = centerPoint
        self.radincr = radiusIncrement
        self.webstats = [self.centerpoint]

        
    def getmousesector(self, mousePLoc):
        # Both hover and click?
        # pyg.draw.circle(self.surface, (255,0,0), mouseLoc, 1, 0)  # Trail of dots following mouse cursor
        mouseR, mouseTheta = mousePLoc
        # Find sector of board #
        for i in xrange(4):
            ring = i+1
            if mouseR < ring * self.radincr:
                sR = ring
                break
            sR = None
        if sR == None:
            sTheta = None
        else:
            sTheta = int(mouseTheta/45) + 1
        return sR, sTheta


class GameView(object):
    """docstring for GameView"""
    def __init__(self):
        super(GameView, self).__init__()
    
        

def stttmain():

    pyg.init()
    pyg.event.get()

    TTTControl = GameController()
    TTTView = GameView()
    TTTModel = GameModel()

    while True:
        TTTControl.currentevents = pyg.event.get()
        quit = TTTControl.exitevents()
        keys = TTTControl.keyboardevents()
        mousepos, mousePolPos, mouseclick = TTTControl.mouseevents()
        print mousepos





if __name__ == '__main__':
    stttmain()