### pygametest1.py ###

import pygame as pyg
from pygame.locals import *

class GameBoard(object):
        """centerPoint - tuple (x,y)."""
        def __init__(self, centerPoint, radiusIncrement):
            super(GameBoard, self).__init__()
            self.centerpoint = self.webCX, self.webCY = centerPoint
            self.radincr = radiusIncrement
            self.webstats = [self.centerpoint]

        def draw(self, surface):
            axisLen = int(self.radincr * 4.5)
            diagOffset = int((axisLen**2/2)**.5)    # Determine length of diagonal lines
            arcBox = int((self.radincr**2/2)**.5)        # Determine length of side of rect to contain arc
            for i in xrange(4): # Draw circles
                pyg.draw.circle(surface, (0,0,0), self.centerpoint, (i+1)*self.radincr, 3)

            pyg.draw.line(surface, (0,0,0), (self.webCX - axisLen,self.webCY), (self.webCX+axisLen, self.webCY), 3)
            pyg.draw.line(surface, (0,0,0), (self.webCX, self.webCY - axisLen), (self.webCX, self.webCY + axisLen), 3)
            pyg.draw.line(surface, (0,0,0), (self.webCX - diagOffset, self.webCY - diagOffset), (self.webCX + diagOffset, self.webCY + diagOffset), 5)
            pyg.draw.line(surface, (0,0,0), (self.webCX + diagOffset, self.webCY - diagOffset), (self.webCX - diagOffset, self.webCY + diagOffset), 5)
          
        def getmouseregion(self):
            # Both hover and click?
                    pass  

        def highlightregion(self, theta, radius, rb):
            if rb == 'r':
                color = (255,0,0)
            elif rb == 'b':
                color = (0,255,0)
            else:
                raise TypeError('Invalid Color selected. Please give highlightregion() either \'r\' or \'b\'')
            # pyg.draw.arc(background, color, 


def main():
    pyg.init()
    screen = pyg.display.set_mode((800, 800))
    pyg.display.set_caption('A test pygame program')
    
    # Fill background
    background = pyg.Surface(screen.get_size())
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

    while True:
        for event in pyg.event.get():
            if event.type == QUIT:
                pyg.quit()
                return

        screen.blit(background, (0, 0))
        pyg.display.flip()

if __name__ == '__main__':
    main()