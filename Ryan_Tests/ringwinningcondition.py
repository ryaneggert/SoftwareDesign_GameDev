from itertools import groupby
from operator import itemgetter

def consecutivelists(checklist):
    conseclists = []
    for k, g in groupby(enumerate(checklist), lambda (i,x):i-x):
        conseclists.append(map(itemgetter(1), g))
    return conseclists

def checkringwin(conseclist):
    won = 0
    for item in conseclist:
        if len(item) >= 4:
            print "Won with ring"
            won = 1
    return won

radii = [3,2,2,1,3,2,2,1,1,4,2]
thetas =[3,1,7,1,3,5,2,3,4,7,8]

ringpieces = {}
for i in xrange(4):
    ringpieces[i+1] = []

for i,radius in enumerate(radii):
    for j in xrange(4):
        if radius == j+1:
            ringpieces[j+1].append(i)

# Check for rings with greater than four
for key,value in ringpieces.iteritems():
    if len(value) > 4:
        # Check for consecutiveness
        checkthetas = []
        for index in value:
            checkthetas.append(thetas[index])
        checkthetas.sort()
        print checkthetas
        conseclist1 = consecutivelists(checkthetas)
        print conseclist1
        won = checkringwin(conseclist1)
        if not won:
            wraparoundthetas = [x if x >3 else x + 8 for x in checkthetas]
            wraparoundthetas.sort()
            print wraparoundthetas
            c = consecutivelists(wraparoundthetas)
            print c
            won = checkringwin(c)
print 'END'
