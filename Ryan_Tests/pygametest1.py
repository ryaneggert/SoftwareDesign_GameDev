### pygametest1.py ###

import pygame as pyg
import math
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
            for i in xrange(4): # Draw circles
                pyg.draw.circle(surface, (0,0,0), self.centerpoint, (i+1)*self.radincr, 3)

            pyg.draw.line(surface, (0,0,0), (self.webCX - axisLen,self.webCY), (self.webCX+axisLen, self.webCY), 3)
            pyg.draw.line(surface, (0,0,0), (self.webCX, self.webCY - axisLen), (self.webCX, self.webCY + axisLen), 3)
            pyg.draw.line(surface, (0,0,0), (self.webCX - diagOffset, self.webCY - diagOffset), (self.webCX + diagOffset, self.webCY + diagOffset), 5)
            pyg.draw.line(surface, (0,0,0), (self.webCX + diagOffset, self.webCY - diagOffset), (self.webCX - diagOffset, self.webCY + diagOffset), 5)
          
        def getmouseregion(self, mousePLoc):
            # Both hover and click?
            # pyg.draw.circle(self.surface, (255,0,0), mouseLoc, 1, 0)  # Trail of dots following mouse cursor
            mouseR, mouseTheta = mousePLoc
            ## Find sector of board ##

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

        def highlightregion(self, theta, radius, rb):
            if rb == 'r':
                color = (255,0,0)
            elif rb == 'b':
                color = (0,255,0)
            else:
                raise TypeError('Invalid Color selected. Please give highlightregion() either \'r\' or \'b\'')
            # pyg.draw.arc(background, color, 


def mousetopolar(mouseLoc, webCenter):
    mx,my = mouseLoc
    cx,cy = webCenter
    rmx = (mx-cx)   # Remapped x (x if the web center is defined now to be the origin)
    rmy = -(my-cy)   # Remapped y (y if the web center is defined now to be the origin)
    mr = math.hypot(rmx, rmy)
    mtheta = math.degrees(math.atan2(rmy,rmx))
    if mtheta < 0:
        mtheta += 360
    return mr, mtheta


def gamescreenmain():
    screen = pyg.display.set_mode((800, 800))   # screen is what is displayed
    pyg.display.set_caption('A test pygame program')
    
    # Fill background
    background = pyg.Surface(screen.get_size()) # background is a surface
    background = background.convert()
    background.fill((250, 250, 250))
    screen.blit(background, (0, 0))

    # Display some text
    font = pyg.font.Font("fonts/RobotoCondensed-Light.ttf", 36)
    text = font.render("Spider Tic-Tac-Toe", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)
    pyg.display.flip()

    # Draw a circle
    webCenter = webCX,webCY = (400,400)   # Coordinate for center of web board
    radIncr = 73
    spiderweb = GameBoard(webCenter, radIncr)
    spiderweb.draw(background)
    screen.blit(background, (0, 0)) # Blit background   
    pyg.display.flip()
    maskt = pyg.mask.from_threshold(background, (0,0,0), (50,50,50))
    maskrects = maskt.get_bounding_rects()
    # for rectangle in maskrects:
    #     pyg.draw.rect(background,(255,120,0), rectangle, 5)

    while True:
        for event in pyg.event.get():
            if event.type == QUIT:
                pyg.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pyg.quit()
                    return
            elif event.type == MOUSEMOTION:     # Only update when mouse moves
                mousePos = mx,my = pyg.mouse.get_pos()     # Current position of mouse cursor
                mousePol = mousetopolar(mousePos, spiderweb.centerpoint)
                print spiderweb.getmouseregion(mousePol)
                # spiderweb.getmouseregion(mousePos)  # Draw dots following the cursor
            elif event.type == MOUSEBUTTONDOWN: # Only register click on mouse button down.
                print 'mousedown'
                lClick = pyg.mouse.get_pressed()[0] # Status of left mouse button
                if lClick == 1:
                    print 'Click'   # May need to debounce

        screen.blit(background, (0, 0)) # Blit background
        pyg.display.flip()

if __name__ == '__main__':
    pyg.init()
    gamescreenmain()