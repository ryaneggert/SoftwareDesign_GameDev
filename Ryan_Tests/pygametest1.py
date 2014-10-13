### pygametest1.py ###

import pygame as pyg
from pygame.locals import *

class Button(object, ):
    """docstring for Button"""
    def __init__(self, arg):
        super(Button, self).__init__()
        self.arg = arg        

def highlightregion(theta, radius):
    pass


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
    axisLen = int(radIncr * 4.5)
    diagOffset = int((axisLen**2/2)**.5)    # Determine length of diagonal lines
    arcBox = int((radIncr**2/2)**.5)        # Determine length of side of rect to contain arc
    for i in xrange(4): # Draw circles
        pyg.draw.circle(background, (0,0,0), webCenter, (i+1)*radIncr, 3)

    pyg.draw.line(background, (0,0,0), (webCX - axisLen,webCY), (webCX+axisLen, webCY), 3)
    pyg.draw.line(background, (0,0,0), (webCX, webCY - axisLen), (webCX, webCY + axisLen), 3)
    pyg.draw.line(background, (0,0,0), (webCX - diagOffset, webCY - diagOffset), (webCX + diagOffset, webCY + diagOffset), 5)
    pyg.draw.line(background, (0,0,0), (webCX + diagOffset, webCY - diagOffset), (webCX - diagOffset, webCY + diagOffset), 5)

    while True:
        for event in pyg.event.get():
            if event.type == QUIT:
                pyg.quit()
                return

        screen.blit(background, (0, 0))
        pyg.display.flip()

if __name__ == '__main__':
    main()