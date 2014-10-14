### misctests.py ###
import itertools, math
sTheta = 3
sR = 2
radincr = 50
corners = []
if sR > 1:
    for i in itertools.product([(sR-1)*radincr, sR * radincr], [sTheta * 45, (sTheta-1) * 45]):
        corners.append(i)
elif sR == 1:
    for i in itertools.product([(sR-1)*radincr, sR * radincr], [sTheta * 45, (sTheta-1) * 45]):
        corners.append(i)
    del corners[0]

avgR = sum(corner[0] for corner in corners)/len(corners)
avgTheta = sum(corner[1] for corner in corners)/len(corners)
avgPol = avgR, avgTheta
avgx = avgR * math.cos(math.radians(avgTheta))
avgy = avgR * math.sin(math.radians(avgTheta))
print int((avgx,avgy))
