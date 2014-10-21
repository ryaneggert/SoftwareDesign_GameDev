## sttt.py ##
# MVC architecture for spider tic-tac-toe

import pygame as pyg
import math, itertools
from pygame.locals import *


class GameController(object):
    """Read events. Send inputs to GameModel object"""

    def __init__(self):
        super(GameController, self).__init__()
        self.mousePos = (None, None)
        self.mousePolPos = (None, None)

    def exitevents(self):
        """Checks for exit events"""
        quit = 0
        for event in self.currentevents:
            if event.type == QUIT:
                quit = 1
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
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
                self.mousepolpos = mousePolPos
                self.mousePos = mousePos
            elif event.type == MOUSEBUTTONDOWN: # Only register click on mouse button down.
                leftClick = pyg.mouse.get_pressed()[0] # Status of left mouse button
                if leftClick == 1:
                    click = 'Left'

        return self.mousePos, self.mousePolPos, click

    def mousecarttopolar(self, mouseLoc, webCenter):
        mX,mY = mouseLoc
        cX,cY = webCenter
        rmX = (mX-cX)   # Remapped x (x if the web center is defined now to be the origin)
        rmY = -(mY-cY)   # Remapped y (y if the web center is defined now to be the origin)
        mr = math.hypot(rmX, rmY)
        mtheta = math.degrees(math.atan2(rmY,rmX))
        if mtheta < 0:
            mtheta += 360
        self.mousePolPos = (mr, mtheta)
        return self.mousePolPos


class GameModel(object):
    """docstring for GameModel"""
    def __init__(self, centerPoint, radiusIncrement, players):
        super(GameModel, self).__init__()
        self.centerpoint = self.webCX, self.webCY = centerPoint
        self.radincr = radiusIncrement
        self.webstats = [self.centerpoint]
        self.numplayers = len(players)
        self.currentplayer = 0
        self.playernames = players
     
    def getmousesector(self, mousePLoc):
        """Takes mouse polar position and outputs the sector of the game board which the mouse is in."""
        # Both hover and click?\
        if mousePLoc == (None, None):
            return mousePLoc
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
        sector = (sR, sTheta)
        return sector

    def sectorcenter(self, sector):
        """Calculates and outputs the geometric center of the input sector of the gameboard in pygame cartesian coordinates."""
        sR, sTheta = sector
        corners = []
        if sR > 1:
            for i in itertools.product([(sR-1)*self.radincr, sR * self.radincr], [sTheta * 45, (sTheta-1) * 45]):
                corners.append(i)
        elif sR == 1:
            for i in itertools.product([(sR-1)*self.radincr, sR * self.radincr], [sTheta * 45, (sTheta-1) * 45]):
                corners.append(i)
            # del corners[0]

        avgR = sum(corner[0] for corner in corners)/len(corners)
        avgTheta = sum(corner[1] for corner in corners)/len(corners)
        avgPol = avgR, avgTheta
        avgX = avgR * math.cos(math.radians(avgTheta))  # Convert to cartesian
        avgY = avgR * math.sin(math.radians(avgTheta))
        screenX = self.webCX + avgX
        screenY = (self.webCY - avgY)
        screenSectorCoords = (int(screenX),int(screenY))
        return screenSectorCoords

    def updategamearray(self, player, sector):
        pass


class GameView(object):
    """docstring for GameView"""
    def __init__(self, centerpoint, radiusIncrement):
        super(GameView, self).__init__()
        self.centerpoint = self.webCX, self.webCY = centerpoint
        self.radincr = radiusIncrement
        self.screen = pyg.display.set_mode((800, 800))   # screen is what is displayed
        pyg.display.set_caption('Spyder Tic-Tac-Toe')
        # Create surface
        background = pyg.Surface(self.screen.get_size()) # background is a surface
        self.background = background.convert()

        # Create global fonts
        self.robotocondensedL = pyg.font.Font("fonts/RobotoCondensed-Light.ttf", 36)
        self.drawweb()
        pyg.display.flip

    def drawweb(self):
        """Draws only the web and title text"""
        axisLen = int(self.radincr * 4.5)
        diagOffset = int((axisLen**2/2)**.5)    # Determine length of diagonal lines
        arcBox = int((self.radincr**2/2)**.5)        # Determine length of side of rect to contain arc
        self.background.fill((250, 250, 250))
        for i in xrange(4): # Draw circles
            pyg.draw.circle(self.background, (0,0,0), self.centerpoint, (i+1)*self.radincr, 3)

        pyg.draw.line(self.background, (0,0,0), (self.webCX - axisLen,self.webCY), (self.webCX+axisLen, self.webCY), 3)
        pyg.draw.line(self.background, (0,0,0), (self.webCX, self.webCY - axisLen), (self.webCX, self.webCY + axisLen), 3)
        pyg.draw.line(self.background, (0,0,0), (self.webCX - diagOffset, self.webCY - diagOffset), (self.webCX + diagOffset, self.webCY + diagOffset), 5)
        pyg.draw.line(self.background, (0,0,0), (self.webCX + diagOffset, self.webCY - diagOffset), (self.webCX - diagOffset, self.webCY + diagOffset), 5)
        text = self.robotocondensedL.render("Spyder Tic-Tac-Toe", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        self.background.blit(text, textpos)
        self.screen.blit(self.background, (0,0))
        
    def drawhovericon(self, sectorcenter, player):
        """Given the cartesian center of a sector of the gameboard, draws a semitransparent icon over that sector """
        pyg.draw.circle(self.background, (0,255,126), sectorcenter, 5, 3)

        
def stttmain(playerNames):
    pyg.init()

    TTTModel = GameModel((400,400), 73, playerNames)
    TTTView = GameView(TTTModel.centerpoint, TTTModel.radincr)
    TTTControl = GameController()

    while True:
        TTTControl.currentevents = pyg.event.get()
        quit = TTTControl.exitevents()
        keys = TTTControl.keyboardevents()
        mousepos, mousePolPos, mouseclick = TTTControl.mouseevents(TTTModel)
        # If we want to quit, then do so.
        if quit:
            print "Quitting"
            pyg.quit()
            return
        # Do some game thinking
        TTTView.drawweb()
        mouseSector = TTTModel.getmousesector(mousePolPos)
        if mouseSector != (None,None):
            mouseSectorCenter = TTTModel.sectorcenter(mouseSector)
            TTTView.drawhovericon(mouseSectorCenter,1)

            
        TTTView.screen.blit(TTTView.background, (0, 0)) # Blit background  # PUT NEXT TWO LINES INTO VIEW?
        pyg.display.flip()




if __name__ == '__main__':
    stttmain(['Abi', 'Meg', 'Ryan'])