### pygametest1.py ###

import pygame as pyg
import math, itertools
from pygame.locals import *

class GameBoard(object):
        """centerPoint - tuple (x,y)."""
        def __init__(self, centerPoint, radiusIncrement):
            super(GameBoard, self).__init__()
            self.centerpoint = self.webCX, self.webCY = centerPoint
            self.radincr = radiusIncrement
            self.webstats = [self.centerpoint]


        def draw(self, surface):
            self.surface = surface
            axisLen = int(self.radincr * 4.5)
            diagOffset = int((axisLen**2/2)**.5)    # Determine length of diagonal lines
            arcBox = int((self.radincr**2/2)**.5)        # Determine length of side of rect to contain arc
            surface.fill((250, 250, 250))
            for i in xrange(4): # Draw circles
                pyg.draw.circle(surface, (0,0,0), self.centerpoint, (i+1)*self.radincr, 3)

            pyg.draw.line(surface, (0,0,0), (self.webCX - axisLen,self.webCY), (self.webCX+axisLen, self.webCY), 3)
            pyg.draw.line(surface, (0,0,0), (self.webCX, self.webCY - axisLen), (self.webCX, self.webCY + axisLen), 3)
            pyg.draw.line(surface, (0,0,0), (self.webCX - diagOffset, self.webCY - diagOffset), (self.webCX + diagOffset, self.webCY + diagOffset), 5)
            pyg.draw.line(surface, (0,0,0), (self.webCX + diagOffset, self.webCY - diagOffset), (self.webCX - diagOffset, self.webCY + diagOffset), 5)
            text = robotocondensedL.render("Spyder Tic-Tac-Toe", 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = surface.get_rect().centerx
            surface.blit(text, textpos)

          
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


        def sectorcenter(self, sector):
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
            return int(screenX),int(screenY)


        def highlightregion(self, theta, radius, rb):
            if rb == 'r':
                color = (255,0,0)
            elif rb == 'b':
                color = (0,255,0)
            else:
                raise TypeError('Invalid Color selected. Please give highlightregion() either \'r\' or \'b\'')



def mousetopolar(mouseLoc, webCenter):
    mX,mY = mouseLoc
    cX,cY = webCenter
    rmX = (mX-cX)   # Remapped x (x if the web center is defined now to be the origin)
    rmY = -(mY-cY)   # Remapped y (y if the web center is defined now to be the origin)
    mr = math.hypot(rmX, rmY)
    mtheta = math.degrees(math.atan2(rmY,rmX))
    if mtheta < 0:
        mtheta += 360
    return mr, mtheta


def gamescreenmain(names):
    screen = pyg.display.set_mode((800, 800))   # screen is what is displayed
    pyg.display.set_caption('Spyder Tic-Tac-Toe')
    
    # Create surface
    background = pyg.Surface(screen.get_size()) # background is a surface
    background = background.convert()

    # Create global fonts
    global robotocondensedL
    robotocondensedL = pyg.font.Font("fonts/RobotoCondensed-Light.ttf", 36)

    # Create gameboard
    webCenter = webCX,webCY = (400,400)   # Coordinate for center of web board
    radIncr = 73
    spiderweb = GameBoard(webCenter, radIncr)

    sectorHist = [(None,None), (None,None)]
    lastsectorHist = []
    # i = 0
    player = 0

    while True:
        # i +=1
        for event in pyg.event.get():
            if event.type == QUIT:
                pyg.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pyg.quit()
                    return
            elif event.type == MOUSEMOTION:     # Only update when mouse moves
                mousePos = mX,mY = pyg.mouse.get_pos()     # Current position of mouse cursor
                mousePol = mousetopolar(mousePos, spiderweb.centerpoint)
                del sectorHist [0]
                sectorHist.append(spiderweb.getmousesector(mousePol))
                # spiderweb.getmouseregion(mousePos)  # Draw dots following the cursor
            elif event.type == MOUSEBUTTONDOWN: # Only register click on mouse button down.
                lClick = pyg.mouse.get_pressed()[0] # Status of left mouse button
                if lClick == 1:
                    print 'Left Click'
                    player +=1
        background.fill((250, 250, 250))
        spiderweb.draw(background)
        if sectorHist[1] != (None, None):
            sectorCenter= spiderweb.sectorcenter(sectorHist[1])
            pyg.draw.circle(background, (0,255,126), sectorCenter, 5, 3)

## Why multiple mouse regs. for sectorhist check?
        # # print lastsectorHist, sectorHist
        # if sectorHist[0] != sectorHist[1] and sectorHist[1] != (None, None):
        #     print i
        #     print 'lsH = '+str(lastsectorHist )+' | sH = ' + str(sectorHist)
        #     if lastsectorHist != sectorHist:
        #         print sectorHist
        #         lastsectorHist = sectorHist
        #     # print spiderweb.sectorcenter(sectorHist[1])

        # Draw player name
        # robotocondensedL.render()
        # text = robotocondensedL.render("Spider Tic-Tac-Toe", 1, (10, 10, 10))
        # textpos = text.get_rect()
        # textpos.centerx = surface.get_rect().centerx
        # surface.blit(text, textpos)
        
        screen.blit(background, (0, 0)) # Blit background
        pyg.display.flip()


if __name__ == '__main__':
    pyg.init()
    gamescreenmain(['Boris Schmidt', 'Heinrich Jones', 'Bjorn McDonald'])