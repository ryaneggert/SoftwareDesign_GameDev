## sttt.py ##
# MVC architecture for spider/spyder tic-tac-toe

import pygame as pyg
import math
import itertools
from pygame.locals import *


class GameController(object):

    """Tic-Tac-Toe game controller component. Read events.
    Send inputs to GameModel object
    """

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
                # Current position of mouse cursor
                mousePos = mX, mY = pyg.mouse.get_pos()
                mousePolPos = self.mousecarttopolar(
                    mousePos, GameBoard.centerpoint)
                self.mousepolpos = mousePolPos
                self.mousePos = mousePos
            # Only register click on mouse button down.
            elif event.type == MOUSEBUTTONDOWN:
                # Status of left mouse button
                leftClick = pyg.mouse.get_pressed()[0]
                if leftClick == 1:
                    click = 'Left'

        return self.mousePos, self.mousePolPos, click

    def mousecarttopolar(self, mouseLoc, gameBoardCenter):
        """Converts a cartesian mouse position to a polar coordinate relative
        to the center of the gameboard
        """
        mX, mY = mouseLoc
        cX, cY = gameBoardCenter
        # Remapped x (x if the gameboard centerpoint is defined now to be the
        # origin)
        rmX = (mX - cX)
        # Remapped y (y if the gameboard centerpoint is defined now to be the
        # origin)
        rmY = -(mY - cY)
        mr = math.hypot(rmX, rmY)
        mtheta = math.degrees(math.atan2(rmY, rmX))
        if mtheta < 0:
            mtheta += 360
        self.mousePolPos = (mr, mtheta)
        return self.mousePolPos


class GameModel(object):

    """Tic-Tac-Toe game model component.
    Calculates and remembers game state.
    """

    def __init__(self, centerPoint, radiusIncrement, players):
        super(GameModel, self).__init__()
        self.centerpoint = self.webCX, self.webCY = centerPoint
        self.radincr = radiusIncrement
        self.webstats = [self.centerpoint]
        self.numplayers = len(players)
        self.currentplayerindex = 0

        self.playernames = players
        playerobjs = []
        i = 0
        for name in players:
            i += 1
            playerobjs.append(Player(name, i))
        self.players = playerobjs   # All the player objects
        self.setcurrentplayer(self.currentplayerindex)

        # Instantiate game array
        full_board = []
        for num in range(4):
            full_board.append([])
            for num2 in range(8):
                full_board[num].append(None)
        # print full_board
        self.boardarray = full_board

    def setcurrentplayer(self, index):
        """Returns a player object given an index (0,1,2)."""
        self.currentplayer = self.players[index]

    def nextplayer(self):
        """Increments the currentplayerindex and sets
        the currentplayer to be the next player.
        """
        currentindex = self.currentplayerindex
        currentindex += 1
        self.currentplayerindex = currentindex % self.numplayers
        self.setcurrentplayer(self.currentplayerindex)

    def getmousesector(self, mousePLoc):
        """Takes mouse polar position and outputs the sector of the
        game board which the mouse is in.
        """
        # Both hover and click?\
        if mousePLoc == (None, None):
            return mousePLoc
        mouseR, mouseTheta = mousePLoc
        # Find sector of board #
        for i in xrange(4):
            ring = i + 1
            if mouseR < ring * self.radincr:
                sR = ring
                break
            sR = None
        if sR is None:
            sTheta = None
        else:
            sTheta = int(mouseTheta / 45) + 1
        sector = (sR, sTheta)
        return sector

    def sectorcenter(self, sector):
        """Calculates and outputs the geometric center of the input sector
        of the gameboard in pygame cartesian coordinates.
        """
        sR, sTheta = sector
        corners = []
        if sR > 1:
            for i in itertools.product([(sR - 1) * self.radincr,
                    sR * self.radincr], [sTheta * 45, (sTheta - 1) * 45]):
                corners.append(i)
        elif sR == 1:
            for i in itertools.product([(sR - 1) * self.radincr,
                    sR * self.radincr], [sTheta * 45, (sTheta - 1) * 45]):
                corners.append(i)
            # del corners[0]

        avgR = sum(corner[0] for corner in corners) / len(corners)
        avgTheta = sum(corner[1] for corner in corners) / len(corners)
        avgPol = avgR, avgTheta
        avgX = avgR * math.cos(math.radians(avgTheta))  # Convert to cartesian
        avgY = avgR * math.sin(math.radians(avgTheta))
        screenX = self.webCX + avgX
        screenY = (self.webCY - avgY)
        screenSectorCoords = (int(screenX), int(screenY))
        return screenSectorCoords

    def placepiece(self, sector):
        """If player clicks, place their icon in the
        gameboard array and their player array
        """
        sR, sTheta = sector
        if self.boardarray[sR - 1][sTheta - 1] is None:
            # Then place piece
            # Update the gameboard array.
            self.boardarray[sR - 1][sTheta - 1] = self.currentplayer.number
            # Add move to this Player's position list
            self.currentplayer.addposition(sector)
            won = self.currentplayer.didwin()
            if not won:
                self.nextplayer()   # Now it's the next person's turn
            return won
        else:
            print "This space is taken"     # For debugging.


class GameView(object):

    """Tic-Tac-Toe game view component. Displays game."""

    def __init__(self, centerpoint, radiusIncrement, playerList):
        super(GameView, self).__init__()
        # Gameboard parameters
        self.centerpoint = self.webCX, self.webCY = centerpoint
        self.radincr = radiusIncrement
        # screen is what is displayed
        self.screen = pyg.display.set_mode((800, 800))
        pyg.display.set_caption('Spyder Tic-Tac-Toe')

        # Create surface
        # background is a surface
        background = pyg.Surface(self.screen.get_size())
        self.background = background.convert()

        # Create global fonts
        self.robotocondensedL = pyg.font.Font(
            "fonts/RobotoCondensed-Light.ttf", 36)
        self.drawweb()
        pyg.display.flip
        imagenames = ['redbug.png', 'bluebug.png', 'purplebug.png']
        playercolors = [(255, 0, 0), (0, 127, 255), (117, 87, 53)]
        # Set Player Icons
        i = 0
        for playerloop in playerList:
            icon = pyg.image.load(imagenames[i])
            playerloop.image = icon
            playerloop.color = playercolors[i]
            i += 1
        self.imagesizes = [0, int(self.radincr * .28), int(self.radincr * .6),
            int(self.radincr * .68), int(self.radincr * .82)]

    def drawweb(self):
        """Draws only the web and title text"""
        axisLen = int(self.radincr * 4.5)
        # Determine length of diagonal lines
        dOff = int((axisLen ** 2 / 2) ** .5)
        # Determine length of side of rect to contain arc
        self.background.fill((250, 250, 250))
        for i in xrange(4):  # Draw circles
            pyg.draw.circle(
                self.background, (0, 0, 0), self.centerpoint,
                (i + 1) * self.radincr, 3)

        pyg.draw.line(self.background, (0, 0, 0), (self.webCX - axisLen,
            self.webCY), (self.webCX + axisLen, self.webCY), 3)
        pyg.draw.line(self.background, (0, 0, 0), (self.webCX,
            self.webCY - axisLen), (self.webCX, self.webCY + axisLen), 3)
        pyg.draw.line(self.background, (0, 0, 0), (self.webCX - dOff,
            self.webCY - dOff), (self.webCX + dOff, self.webCY + dOff), 5)
        pyg.draw.line(self.background, (0, 0, 0), (self.webCX + dOff,
            self.webCY - dOff), (self.webCX - dOff, self.webCY + dOff), 5)
        text = self.robotocondensedL.render(
            "Spyder Tic-Tac-Toe", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        self.background.blit(text, textpos)
        self.screen.blit(self.background, (0, 0))

    def drawhovericon(self, sectorcenter, player):
        """Given the cartesian center of a sector of the gameboard,
        draws a semitransparent icon over that sector.
        """
        pyg.draw.circle(self.background, (0, 255, 126), sectorcenter, 5, 3)

    def place_bug(self, player, sectorcenter, sector):
        # Changes color of dinosaur based on which players turn it is
        sectorX, sectorY = sectorcenter
        sR = sector[0]
        imageSize = (self.imagesizes[sR], self.imagesizes[sR])
        iconDraw = pyg.transform.scale(player.image, imageSize)
        imgSizeX, imgSizeY = imageSize
        position = (sectorX - imgSizeX / 2, sectorY - imgSizeY / 2)
        self.background.blit(iconDraw, position)

    def drawplayername(self, name, color):
        """Draws the name of the current player in the
        current player's color on the screen.
        """
        self.background.blit(
            self.robotocondensedL.render(name, True, color), (650, 730))
        pass

    def drawgamearray(self, playerList, sectormethod):
        """Draws all of the pieces on the board."""
        for playerloop in playerList:
            for position in playerloop.positions:
                self.place_bug(playerloop, sectormethod(position), position)

    def finalizedisplay(self):
        # Blit all background changes to screen
        self.screen.blit(self.background, (0, 0))
        pyg.display.flip()


class Player(object):

    """docstring for Player"""

    def __init__(self, name, number):
        super(Player, self).__init__()
        self.name = name
        self.number = number    # e.g. 1, 2, or 3
        self.positions = []     # Player array
        self.thetas = []
        self.radii = []
        self.color = None

    def setimage(self, imagefilename):
        """Given a filename, sets this Player's icon/image."""
        self.image = pyg.image.load(imagefilename)

    def addposition(self, sector):
        """Add a position to this Player's list of positions"""
        self.positions.append(sector)
        self.thetas.append(sector[1])   # For straight winning condition
        self.radii.append(sector[0])    # For curved winning condition

    def didwin(self):
        """Checks this Player's positions to see if he/she has won."""
        # Straight
        for num in range(8):
            appear = self.thetas.count(num)
            if appear == 4:
                print self.name + ' won with a straight!'    # Debuggging
                return 1


def stttmain(playerNames):
    pyg.init()

    TTTModel = GameModel((400, 400), 73, playerNames)
    TTTView = GameView(
        TTTModel.centerpoint, TTTModel.radincr, TTTModel.players)
    TTTControl = GameController()
    won = 0
    while True:
        TTTControl.currentevents = pyg.event.get()
        quit = TTTControl.exitevents()
        keys = TTTControl.keyboardevents()
        mousepos, mousePolPos, mouseclick = TTTControl.mouseevents(TTTModel)
        # If we want to quit, then do so.
        if quit:
            print "Quitting"
            pyg.quit()
            # print TTTModel.boardarray
            return
        # Do some game thinking
        TTTView.drawweb()
        mouseSector = TTTModel.getmousesector(mousePolPos)
        # print TTTModel.currentplayer.name
        TTTView.drawplayername(
            TTTModel.currentplayer.name, TTTModel.currentplayer.color)
        if mouseSector != (None, None):
            mouseSectorCenter = TTTModel.sectorcenter(mouseSector)
            # TTTView.drawhovericon(mouseSectorCenter,1)
            TTTView.place_bug(
                TTTModel.currentplayer, mouseSectorCenter, mouseSector)
            if mouseclick == 'Left':
                won = TTTModel.placepiece(mouseSector)

        # Finalize Display
        # Draw entire gameboard
        TTTView.drawgamearray(TTTModel.players, TTTModel.sectorcenter)
        TTTView.finalizedisplay()
        if won:
            return


if __name__ == '__main__':
    stttmain(['Abi', 'Meg', 'Ryan'])
