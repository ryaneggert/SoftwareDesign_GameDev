## sttt.py ##
# MVC architecture for spider/spyder tic-tac-toe

import pygame as pyg
import welcome
import math
import itertools
from operator import itemgetter
from pygame.locals import *


class GameController(object):

    """Tic-Tac-Toe game controller component. Read events.
    Send inputs to GameModel object
    """

    def __init__(self):
        super(GameController, self).__init__()
        self.mousepos = (None, None)
        self.mousepolpos = (None, None)
        self.mouseclick = None
        self.quitgame = 0

    def exitevents(self):
        """Checks for exit events"""
        quitgame = 0
        for event in self.currentevents:
            if event.type == QUIT:
                quitgame = 1
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quitgame = 1
        self.quitgame = quitgame

    def keyboardevents(self):
        """Checks for keyboard input"""
        keyInput = None
        for event in self.currentevents:
            if event.type == KEYDOWN and event.key != K_ESCAPE:
                keyInput = event.key
        self.keyinput = keyInput

    def mouseevents(self, GameBoard):
        """Handles mouse events (clicks and position)"""
        click = None
        mousepos = None
        for event in self.currentevents:
            if event.type == MOUSEMOTION:   # Only update when mouse moves
                # Current position of mouse cursor
                mousePos = mX, mY = pyg.mouse.get_pos()
                mousePolPos = self.mousecarttopolar(
                    mousePos, GameBoard.centerpoint)
                self.mousepolpos = mousePolPos
                self.mousepos = mousePos
            # Only register click on mouse button down.
            elif event.type == MOUSEBUTTONDOWN:
                # Status of left mouse button
                leftClick = pyg.mouse.get_pressed()[0]
                if leftClick == 1:
                    click = 'Left'
        self.mouseclick = click

    def consolekeys(self):
        """Prints read character keystrokes to the console."""
        if self.keyinput is not None:
            if self.keyinput < 129:
                print str(unichr(self.keyinput))
            else:
                print 'char(%s)' % self.keyinput

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
        pyg.display.flip()

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
        pyg.draw.circle(self.background, player.color, sectorcenter, 5, 3)

    def place_bug(self, player, sectorcenter, sector):
        # Changes color of dinosaur based on which players turn it is
        sectorX, sectorY = sectorcenter
        sR = sector[0]
        imageSize = (self.imagesizes[sR], self.imagesizes[sR])
        iconDraw = pyg.transform.scale(player.image, imageSize)
        imgSizeX, imgSizeY = imageSize
        position = (sectorX - imgSizeX / 2, sectorY - imgSizeY / 2)
        self.background.blit(iconDraw, position)

    def drawplayername(self, name, pcolor):
        """Draws the name of the current player in the
        current player's color on the screen.
        """
        self.background.blit(
            self.robotocondensedL.render(name, True, pcolor), (20, 730))

    def drawgamearray(self, player_list, sectormethod):
        """Draws all of the pieces on the board."""
        for playerloop in player_list:
            for position in playerloop.positions:
                self.place_bug(playerloop, sectormethod(position), position)

    def finalizedisplay(self):
        # Blit all background changes to screen
        self.screen.blit(self.background, (0, 0))
        pyg.display.flip()

    def winningpopup(self, playername, mouseposition, mouseclick):
        # print "win"
        a = 0
        trans = pyg.Surface((600, 400))  # starts at (0,0) and builds (width,height)
        trans.set_alpha(235)
        trans.fill((60,60,60))
        self.background.blit(trans, (100,200))
        font = pyg.font.Font(None, 36)
        winning_msg = 'Congratulations ' + playername + '!'
        default_msg = 'You won the game!'
        self.font = pyg.font.SysFont('robotocondensedL', 50)
        text = self.font.render(winning_msg, True, (255,255,255))
        textrect = text.get_rect()
        textrect.centerx = self.background.get_rect().centerx
        textrect.centery = self.background.get_rect().centery
        self.background.blit(text, textrect)
        self.background.blit(self.font.render(default_msg, True, (255,255,255)), (250,500))
        self.main_menu = welcome.Button()
        self.quitting = welcome.Button()

        self.main_menu.create_button(self.background, (0, 255, 0), 220, 220, 160, 100, 0, "Menu", (0, 0, 0))
        self.quitting.create_button(self.background, (0, 255, 0), 420, 220, 160, 100, 0, "Exit", (0, 0, 0))
        
        if mouseclick == 'Left':
            if self.main_menu.pressed(mouseposition):
                a = 2
                return a
            elif self.quitting.pressed(mouseposition):
                a = 1
                return a

        #print self.name + ' won with a straight!'

class Player(object):

    """Player object."""

    def __init__(self, name, number):
        super(Player, self).__init__()
        self.name = name
        self.number = number    # e.g. 1, 2, or 3
        self.positions = []     # Player array
        self.thetas = []
        self.radii = []
        self.color = None
        self.image = None

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
        strwin = self.straightwin()
        curwin = self.curvedwin()
        diawin = self.diagwin()
        # for radius in self.radii:
        if strwin or curwin or diawin:
            win = 1
        else:
            win = 0
        return win

    def straightwin(self):
        won = 0
        for num in range(8):
            appear = self.thetas.count(num)
            if appear == 4:
                print self.name + ' won with a straight!'    # Debugging
                won = 1
        return won

    def curvedwin(self):
        won = 0
        ringpieces = {}
        for i in xrange(4):
            ringpieces[i+1] = []

        for i,radius in enumerate(self.radii):
            for j in xrange(4):
                if radius == j+1:
                    ringpieces[j+1].append(i)

        # Check for rings with greater than four
        for key,value in ringpieces.iteritems():
            if len(value) >= 4:
                # Check for consecutiveness
                checkthetas = []
                for index in value:
                    checkthetas.append(self.thetas[index])
                checkthetas.sort()
                conseclist1 = self.consecutivelists(checkthetas)
                won = self.checkringwin(conseclist1)
                if not won:
                    wraparoundthetas = [x if x >3 else x + 8 for x in checkthetas]
                    wraparoundthetas.sort()
                    c = self.consecutivelists(wraparoundthetas)
                    won = self.checkringwin(c)
        return won

    def diagwin(self):
        diagwins = [[(1,1),(2, 2), (3, 3), (4, 4)],
                    [(1,2),(2, 3), (3, 4), (4, 5)],
                    [(1,3),(2, 4), (3, 5), (4, 6)],
                    [(1,4),(2, 5), (3, 6), (4, 7)],
                    [(1,5),(2, 6), (3, 7), (4, 8)],
                    [(1,6),(2, 7), (3, 8), (4, 1)],
                    [(1,7),(2, 8), (3, 1), (4, 2)], 
                    [(1,8),(2, 1), (3, 2), (4, 3)],
                    [(1,8),(2, 7), (3, 6), (4, 5)],
                    [(1,7),(2, 6), (3, 5), (4, 4)],
                    [(1,6),(2, 5), (3, 4), (4, 3)],
                    [(1,5),(2, 4), (3, 3), (4, 2)],
                    [(1,4),(2, 3), (3, 2), (4, 1)],
                    [(1,3),(2, 2), (3, 1), (4, 8)],
                    [(1,2),(2, 1), (3, 8), (4, 7)],
                    [(1,1),(2, 8), (3, 7), (4, 6)]]

        for diagwinningcondition in diagwins:
            won = all(position in self.positions for position in diagwinningcondition)
            if won:
                break
        return won


    def consecutivelists(self,checklist):
        conseclists = []
        for k, g in itertools.groupby(enumerate(checklist), lambda (i,x):i-x):
            conseclists.append(map(itemgetter(1), g))
        return conseclists

    def checkringwin(self,conseclist):
        won = 0
        for item in conseclist:
            if len(item) >= 4:
                print "Won with ring"
                won = 1
        return won


def stttmain(playerNames):
    pyg.init()

    TTTModel = GameModel((400, 400), 73, playerNames)
    TTTView = GameView(
        TTTModel.centerpoint, TTTModel.radincr, TTTModel.players)
    TTTControl = GameController()
    won = 0
    winning_exit = 0
    while True:
        TTTControl.currentevents = pyg.event.get()
        TTTControl.exitevents()
        TTTControl.keyboardevents()
        TTTControl.mouseevents(TTTModel)
        TTTControl.consolekeys()
        # If we want to quit, then do so.
        
        if TTTControl.quitgame:
            print "Quitting"
            pyg.quit()
            # print TTTModel.boardarray
            return
        # Do some game thinking
        TTTView.drawweb()
        mouseSector = TTTModel.getmousesector(TTTControl.mousepolpos)
        # print TTTModel.currentplayer.name
        TTTView.drawplayername(
            TTTModel.currentplayer.name, TTTModel.currentplayer.color)
        if mouseSector != (None, None):
            mouseSectorCenter = TTTModel.sectorcenter(mouseSector)
            # TTTView.drawhovericon(mouseSectorCenter,1)
            TTTView.place_bug(
                TTTModel.currentplayer, mouseSectorCenter, mouseSector)
            if TTTControl.mouseclick == 'Left':
                won = TTTModel.placepiece(mouseSector)      

        # Finalize Display
        # Draw entire gameboard
        
        TTTView.drawgamearray(TTTModel.players, TTTModel.sectorcenter)    
        TTTView.finalizedisplay()
        if won:
            break

    while won:
        TTTControl.currentevents = pyg.event.get()
        TTTControl.exitevents()
        TTTControl.keyboardevents()
        TTTControl.mouseevents(TTTModel)
        TTTControl.consolekeys()
        
        # print winning_exit
        TTTView.drawweb()
        TTTView.drawgamearray(TTTModel.players, TTTModel.sectorcenter)
        TTTView.drawplayername(TTTModel.currentplayer.name, TTTModel.currentplayer.color)
        a = TTTView.winningpopup(TTTModel.currentplayer.name, TTTControl.mousepos, TTTControl.mouseclick)    
        TTTView.finalizedisplay()
        if TTTControl.quitgame or a == 1:
            print "Quitting"
            pyg.quit() 
            return
        elif a == 2:
            welcome.welcome_main()
            return

if __name__ == '__main__':
    stttmain(['Abi', 'Meg', 'Ryan'])
