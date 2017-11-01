
import sys
sys.path.append("..")

from matplotlib import pyplot as plt
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

import svg
import blenderMesh as bm

startX = 7.0
startY = 5.0

svgHeight = 744.09448
#svgScale = 34.9283765 * 1.048689138 # PDF Version: svgUnits per Meter
svgScale = 34.9283765 # Inkscape version: svgUnits per Meter

roomFontSize = 14

def rect(x1, y1, x2, y2):
    global polygon
    xx1 = startX + x1
    yy1 = startY + y1
    xx2 = startX + x2
    yy2 = startY + y2
    coords = [(xx1, yy1), (xx2, yy1), (xx2, yy2), (xx1, yy2)]
    p = Polygon(coords)
    if (polygon == None):
        polygon = p
    else:
        polygon = polygon.union(p)


def wall(x1, y1, x2, y2, name = "wall", color=(0.5, 0.5, 0.5)):
    global etage
    rect(x1, y1, x2, y2)    
    mf.quad(name, (x1,y1,etage * etageHeight), (x2,y2,(etage * etageHeight + wallHeight)), color)

def difference(pt1, pt2, diffName, surroundingWallName = "wall"):
    global etage
    x1 = pt1[0]
    y1 = pt1[1]
    z1 = pt1[2]
    x2 = pt2[0]
    y2 = pt2[1]
    z2 = pt2[2]
    plt.plot((10*(startX+x1), 10*(startX+x2), 10*(startX+x2), 10*(startX+x1), 10*(startX+x1)), (10*(startY+y1), 10*(startY+y1), 10*(startY+y2), 10*(startY+y2), 10*(startY+y1)), '-k')
    if (z1 < 1.4) and (z2 > 1.5):
	    svgFile.writeRect(svgScale*(startX+x1), svgHeight-svgScale*(startY+y2), svgScale*(x2-x1), svgScale*(y2-y1), "#bbbbbb")
    pt1 = (x1, y1, etage * etageHeight + z1)
    pt2 = (x2, y2, etage * etageHeight + z2)
    mf.difference(pt1, pt2, diffName, surroundingWallName)

def line(x1, y1, x2, y2):
    x1 = x1 + startX
    y1 = y1 + startY
    x2 = x2 + startX
    y2 = y2 + startY
    plt.plot((10*x1, 10*x2), (10*y1, 10*y2), '-k')
    svgFile.writePolygon((svgScale*x1, svgHeight-svgScale*y1, svgScale*x2, svgHeight-svgScale*y2))

def text(x, y, text, svgFontSize = 9):
    x = x + startX
    y = y + startY
    svgFile.writeText(text, svgScale*x, svgHeight-svgScale*y, 0, svgFontSize)
    plt.text(10*x, 10*y, text)

def measureLine(x, y, align, length, skewLineWidth, scaling = 1):
    ofsX = 0.4
    ofsY = 0.4
    if (align == 'h'):
        ofsX = -0.15
        ofsY = -0.4
    else:
        ofsX = -0.4
        ofsY = -0.15
        pass
    x2 = x + (length if (align == 'h') else 0)
    y2 = y + (length if (align == 'v') else 0)
    line(x, y, x2, y2)
    line(x-skewLineWidth,y-skewLineWidth,x+skewLineWidth,y+skewLineWidth)    
    line(x2-skewLineWidth,y2-skewLineWidth,x2+skewLineWidth,y2+skewLineWidth)
    text((x+x2) / 2.0 + ofsX, (y+y2) / 2.0 + ofsY, str(length * scaling), 9)    

def drawStairs(x, y, align, numStairs, stairWidth, stairDepth):
    global mf
    if (align == 'v'):
        line(x, y, x, y+numStairs*stairDepth)
        line(x+stairWidth, y, x+stairWidth, y+numStairs*stairDepth)
    else:
        line(x, y, x+numStairs*stairDepth, y)
        line(x, y+stairWidth, x+numStairs*stairDepth, y+stairWidth)
    for i in range(0, numStairs + 1):
        if (align == 'v'):
            line(x, y+i*stairDepth, x+stairWidth, y+i*stairDepth)
            mf.quad("stair", (x, (y+i*stairDepth), stairHeight*i), ((x+stairWidth), (y+(i+1)*stairDepth), stairHeight*(i+1)))
        else:
            line(x+i*stairDepth, y, x+i*stairDepth, y+stairWidth)
            mf.quad("stair", ((x+i*stairDepth), y, (stairHeight*(2*numStairs-i))), ((x+(i+1)*stairDepth), (y+stairWidth), stairHeight*(2*numStairs-i+1)))

def savePolygonAsSVG_flipY(xyCoords):
    global svgFile
    cc = list()
    for i in range(0, len(xyCoords[0])):
        cc.append(svgScale*xyCoords[0][i])
        cc.append(svgHeight-svgScale*xyCoords[1][i])
    svgFile.writePolygon(cc)

def savePolygonAsSVG(pp):
    global svgFile
    if (type(pp) == Polygon):
        savePolygonAsSVG_flipY(pp.exterior.coords.xy)
        for p in pp.interiors:
            savePolygonAsSVG_flipY(p.coords.xy)
    else:
        for subP in pp:
            savePolygonAsSVG_flipY(subP.exterior.coords.xy)
            for p in subP.interiors:
                savePolygonAsSVG_flipY(p.coords.xy)

def pltSinglePoly(xy):
    xx = list()
    yy = list()
    for x in xy[0]:
        xx.append(x*10)
    for y in xy[1]:
        yy.append(y*10)
    plt.plot(xx, yy, '-k')

def pltPolygon(pp):
    if (type(pp) == Polygon):
        pltSinglePoly(pp.exterior.coords.xy)
        for p in pp.interiors:
            pltSinglePoly(p.coords.xy)
    else:
        for subP in pp:
            pltSinglePoly(subP.exterior.coords.xy)
            for p in subP.interiors:
                pltSinglePoly(p.coords.xy)

				
####################################################################
### GROUND FLOOR ###################################################
####################################################################

etageHeight = 3.0
wallHeight = 2.6
etageMinusWall = etageHeight - wallHeight
etage = 0

svgFile = svg.SVG()
svgFile.openFile("plan_groundFloor.svg")

fig = plt.figure(1, figsize=(20,6), dpi=90)
ax = fig.add_subplot(111)

mf = bm.MeshFile()
mf.openFile("blenderGen.py")

polygon = None


# units: 1 = 1m

houseWidth = 14
houseHeight = 10


outWallThick = 0.5
innerWallThick = 0.25
owt = outWallThick
iwt = innerWallThick

# Title (ground floor)
text(3, 12, "Erdgeschoss", 20)

# outer walls of house
wall(owt, 0, houseWidth-owt, owt, "ground_w1")
wall(owt, houseHeight-owt, houseWidth-owt, houseHeight, "ground_w2")
wall(0, 0, owt, houseHeight, "ground_w3")
wall(houseWidth-owt, 0, houseWidth, houseHeight, "ground_w4")
difference((0.8, 0, 0), (5.2, owt, 2.25), "garageDoor", "ground_w1")  # garage door
difference((6.5, 0, 0), (7.7, owt, 2.1), "mainEntrance", "ground_w1")  # main house entrance door
difference((8.4, 0, 1.2), (9.4, owt, 2.0), "window1", "ground_w1")  # window 1
difference((12.0, 0, 1.2), (13.0, owt, 2.0), "window2", "ground_w1")  # window 2

# garage 
garageWidth = 5.0
wall(garageWidth+owt, owt, garageWidth+owt+iwt, houseHeight-owt)
text(2.0, 3.0, "Garage", roomFontSize)

# room right bottom (room 1)
room1Width = 3.5
room1Height = 3.0
r1_x = houseWidth - owt - room1Width - iwt
r1_y = room1Height + owt + iwt
wall(r1_x, owt, r1_x + iwt, r1_y)
wall(r1_x, r1_y - iwt, houseWidth, r1_y)
text(r1_x + 1.0, r1_y - 2.0, "Zi 1", roomFontSize)

# room2 in ground floor
room2Width = 3.5
room2Height = 3.0
r2_x = houseWidth - owt - room2Width - iwt
r2_y = r1_y + iwt + room2Height
wall(r2_x, r1_y, r2_x + iwt, r2_y)
wall(r2_x, r2_y - iwt, houseWidth, r2_y)
text(r2_x + 1.0, r2_y - 2.0, "Zi 2", roomFontSize)

# room3 in ground floor
room3Width = 3.5
room3Height = 2.5
r3_x = houseWidth - owt - room3Width - iwt
r3_y = r2_y + iwt + room3Height
wall(r3_x, r2_y, r3_x + iwt, r3_y)
wall(r3_x, r3_y - iwt, houseWidth, r3_y)
text(r3_x + 1.0, r3_y - 2.0, "Zi 3", roomFontSize)

# stairs
stairDepth = 0.27
stairWidth = 1.12
stairHeight = 0.185
stairsX = houseWidth - owt - iwt - room1Width - 2 * stairWidth
stairsX = stairsX + 1.2
stairsY = 5.0
drawStairs(stairsX, stairsY - stairDepth * 8, 'v', 8, stairWidth, stairDepth)
drawStairs(stairsX - stairDepth * 8, stairsY, 'h', 7, stairWidth, stairDepth)
line(stairsX+stairWidth, stairsY, stairsX+stairWidth, stairsY+stairWidth)
line(stairsX, stairsY+stairWidth, stairsX+stairWidth, stairsY+stairWidth)


# bottom of ground floor
mf.quad("base", (0, 0, -0.4), (houseWidth, houseHeight, 0))

# bounding box of lower part of house
mf.quad("houseBoundingBox", (0.0, 0.0, -0.4), (houseWidth, houseHeight, 5.0), (1, 1, 0.0))
mf.setVisible("houseBoundingBox", False)
mf.quad("Vorplatz", (0.0, -8, 0.0), (houseWidth, 1.0, 5.0), (1, 1, 0.0))
mf.setVisible("Vorplatz", False)

# mesure lines

xAcc = 0
measureLine(0, -2, 'h', 14, 0.2)
measureLine(xAcc, -1, 'h', owt, 0.2)
xAcc = xAcc + owt
measureLine(xAcc, -1, 'h', garageWidth, 0.2)
xAcc = xAcc + garageWidth
measureLine(xAcc, -1, 'h', iwt, 0.2)
xAcc = xAcc + iwt
stairWayWidth = houseWidth - (2*owt+garageWidth+2*iwt+room1Width)
measureLine(xAcc, -1, 'h', stairWayWidth, 0.2)
xAcc = xAcc + stairWayWidth
measureLine(xAcc, -1, 'h', iwt, 0.2)
xAcc = xAcc + iwt
measureLine(xAcc, -1, 'h', room1Width, 0.2)
xAcc = xAcc + room1Width
measureLine(xAcc, -1, 'h', owt, 0.2)

measureLine(-1.0, 0, 'v', 10, 0.2)

#patch = None
#if (type(polygon) == Polygon):
#    patch = PolygonPatch(polygon, facecolor='#DDDDDD', edgecolor='#000000', alpha=1.0, zorder=2)
#    ax.add_patch(patch)
#else:
#    for p in polygon:
#        patch = PolygonPatch(p, facecolor='#DDDDDD', edgecolor='#000000', alpha=1.0, zorder=2)
#        ax.add_patch(patch)

pltPolygon(polygon)

xrange = [-1, 300]
yrange = [-1, 200]
ax.set_xlim(*xrange)
#ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(*yrange)
#ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)

plt.show()

savePolygonAsSVG(polygon)

svgFile.closeFile()

####################################################################
### FIRST FLOOR AND ROOF ###########################################
####################################################################

etage = 1

fig = plt.figure(2, figsize=(20,6), dpi=90)
ax = fig.add_subplot(111)

polygon = None

svgFile = svg.SVG()
svgFile.openFile("plan_firstFloor.svg")

# Title (first floor)
text(3, 12, "Erster Stock", 20)


# outer walls of house
brown = (0.95, 0.4, 0.13)
wall(owt, 0, houseWidth-owt, owt, name="first_w1", color=brown)
difference((0.8, 0, 0), (3.8, owt, 2.25), "terrasseDoorSouth", "first_w1")  # terrasseDoorSouth
difference((6.5, 0, 1.0), (7.3, owt, 2.0), "window3", "first_w1")  # window 3
difference((8.4, 0, 1.0), (9.2, owt, 2.0), "window4", "first_w1")  # window 4
difference((12.0, 0, 1.0), (12.8, owt, 2.0), "window5", "first_w1")  # window 5
wall(owt, houseHeight-owt, houseWidth-owt, houseHeight, name="first_w2", color=brown)
wall(0, 0, owt, houseHeight, name="first_w3", color=brown)
difference((0, 1.0, 0), (owt, 4.0, 2.25), "terrasseDoorWest", "first_w3")  # terrasseDoorWest
difference((0, 7.4, 1.0), (owt, 9.0, 2.25), "window6", "first_w3")  # window 6
wall(houseWidth-owt, 0, houseWidth, houseHeight, name="first_w4", color=brown)


# stairs
drawStairs(stairsX, stairsY - stairDepth * 8, 'v', 8, stairWidth, stairDepth)
drawStairs(stairsX - stairDepth * 8, stairsY, 'h', 7, stairWidth, stairDepth)
line(stairsX+stairWidth, stairsY, stairsX+stairWidth, stairsY+stairWidth)
line(stairsX, stairsY+stairWidth, stairsX+stairWidth, stairsY+stairWidth)

wall(garageWidth+owt, owt, garageWidth+owt+iwt, houseHeight-owt, name="wallWZ", color=brown)
difference((garageWidth+owt, 4.0, 0.0), (garageWidth+owt+iwt, 6-0, 2.0), "doorLivingRoom", "wallWZ")  # doorLivingRoom
text(3.0, 3.0, "Wohnzimmer", roomFontSize)

mf.quad("baseFirstFloor", (0, 0, wallHeight), (houseWidth, houseHeight, etageHeight))
difference((garageWidth+owt*2+1.0, 4.9, -1.0), (garageWidth+owt*2+4.0, 6.1, 1.0), "stairsHole", "baseFirstFloor")  # hole for stairs in floor of first floor

# Balkon
mf.quad("Balkon", (0, -2, wallHeight), (4, 0, etageHeight))

# Terrasse
mf.quad("Terrasse", (-4, -2, 0), (0, 10, etageHeight))

### ROOF

mf.quad("roofBase", (0, 0, (etageHeight + wallHeight)), (houseWidth, houseHeight, etageHeight * 2), color=brown)
ptsRF = list()
ofsX = 0.5
ofsY = 0.5
roofStartHeight = etageHeight * 2
roofHeight = 2.0
ptsRF.append((-ofsX, -ofsY, roofStartHeight))
ptsRF.append((ofsX + houseWidth, -ofsY, roofStartHeight))
ptsRF.append((ofsX + houseWidth, houseHeight * 0.5, roofStartHeight))
ptsRF.append((-ofsX, houseHeight * 0.5, roofStartHeight))
ptsRF.append((-ofsX, -ofsY, roofStartHeight+0.1))
ptsRF.append((ofsX + houseWidth, -ofsY, roofStartHeight+0.1))
ptsRF.append((ofsX + houseWidth, houseHeight * 0.5, roofStartHeight+roofHeight))
ptsRF.append((-ofsX, houseHeight * 0.5, roofStartHeight+roofHeight))
mf.deformedQuad("roofFront", ptsRF, (1, 0, 0))

ptsRB = list()
ptsRB.append((-ofsX, houseHeight*0.5, roofStartHeight))
ptsRB.append((ofsX + houseWidth , houseHeight*0.5, roofStartHeight))
ptsRB.append((ofsX + houseWidth, ofsY + houseHeight, roofStartHeight))
ptsRB.append((-ofsX, ofsY + houseHeight, roofStartHeight))
ptsRB.append((-ofsX, houseHeight*0.5, roofStartHeight+roofHeight))
ptsRB.append((ofsX + houseWidth , houseHeight*0.5, roofStartHeight+roofHeight))
ptsRB.append((ofsX + houseWidth, ofsY + houseHeight, roofStartHeight))
ptsRB.append((-ofsX, ofsY + houseHeight, roofStartHeight))
mf.deformedQuad("roofFront", ptsRB, (1, 0, 0))


### Measure Lines

measureLine(0, -2, 'h', 14, 0.2,)
measureLine(0, -1, 'h', owt, 0.2,)
measureLine(owt, -1, 'h', garageWidth, 0.2)
measureLine(owt+garageWidth, -1, 'h', iwt, 0.2)
measureLine(owt+garageWidth+iwt, -1, 'h', 4, 0.2)

measureLine(-1.0, 0, 'v', 10, 0.2)



#patch = None
#if (type(polygon) == Polygon):
#    patch = PolygonPatch(polygon, facecolor='#DDDDDD', edgecolor='#000000', alpha=1.0, zorder=2)
#    ax.add_patch(patch)
#else:
#    for p in polygon:
#        patch = PolygonPatch(p, facecolor='#DDDDDD', edgecolor='#000000', alpha=1.0, zorder=2)
#        ax.add_patch(patch)

pltPolygon(polygon)


xrange = [-1, 300]
yrange = [-1, 200]
ax.set_xlim(*xrange)
#ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(*yrange)
#ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)

plt.show()

savePolygonAsSVG(polygon)

svgFile.closeFile()

mf.closeFile()

####################################################################
####################################################################
####################################################################



