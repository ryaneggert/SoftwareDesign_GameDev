### polarconversiontest.py ###
import math

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

def main():
    print mousetopolar((560,575), (400,400))




if __name__ == '__main__':
    main()