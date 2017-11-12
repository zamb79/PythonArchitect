
import sys
sys.path.append("..")

import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

import svg
import blenderMesh as bm
import architecture as ar

ar.startX = 7.0
ar.startY = 5.0

ar.svgHeight = 744.09448
#ar.svgScale = 34.9283765 * 1.048689138 # PDF Version: svgUnits per Meter
ar.svgScale = 34.9283765 # Inkscape version: svgUnits per Meter

roomFontSize = 14

ar.etageHeight = 3.0
ar.wallHeight = 2.6
ar.etageCeilHeight = ar.etageHeight - ar.wallHeight
ar.etage = 0

ar.initSvgFile("generatedFiles/plan_groundFloor.svg")
ar.initMeshFile("generatedFiles/generateCad.py")

# units: 1 = 1m

houseWidth = 14.0
houseHeight = 10.0

outWallThick = 0.5
innerWallThick = 0.25
owt = outWallThick
iwt = innerWallThick

				
####################################################################
### CREATE TERRAIN #################################################
####################################################################

# Coordinates in file are relative to 105000.0 m in X and 314150.0 m in Y

# rotate and move to good origin
pts = np.genfromtxt('points.csv', delimiter=",") - [1, 10.5, 429]
a = np.pi / 180.0 * -19.3
pXY = pts[:,0:2] * np.mat([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])
pXY = pXY
pZ = np.mat(pts[:,2]).T
ptsTransformed = np.asarray(np.concatenate([pXY, pZ], 1))
gapToStreet = 4.0
ptsTransformed = ptsTransformed - [0, gapToStreet, 0]
ptsBottom = np.concatenate([ptsTransformed[:,0:2], np.zeros((pXY.shape[0], 1))-3], 1)
groundPts = np.concatenate([ptsTransformed, ptsBottom])

faces = list()
for i in range(0, 5):
    for j in range(0, 4):
        idx1 = i * 5 + j
        idx2 = i * 5 + j + 1
        idx3 = (i+1) * 5 + j
        idx4 = (i+1) * 5 + j + 1
        faces.append([idx1, idx2, idx3])
        faces.append([idx2, idx4, idx3])
        faces.append([idx1+30, idx3+30, idx2+30])
        faces.append([idx2+30, idx3+30, idx4+30])

groundBorderPts = [0, 1, 2, 3, 4, 9, 14, 19, 24, 29, 28, 27, 26, 25, 20, 15, 10, 5, 0]
for i in range(0, len(groundBorderPts)):
    idx1 = groundBorderPts[i]
    idx2 = groundBorderPts[i]+30
    idx3 = groundBorderPts[(i+1)%len(groundBorderPts)]+30
    idx4 = groundBorderPts[(i+1)%len(groundBorderPts)]
    faces.append([idx1, idx2, idx3])
    faces.append([idx3, idx4, idx1])

ar.mf.mesh("ground", groundPts, faces, (0.8, 1.0, 0.0))

# cut out the house from the ground
ar.mf.difference((-4, -10, 0), (houseWidth, houseHeight, 5), "houseBox", "ground")  # garage door
ar.mf.difference((0, 0, -0.4), (houseWidth, houseHeight, 1), "houseBoxFloor", "ground")  # garage door

				
####################################################################
### GROUND FLOOR ###################################################
####################################################################

fig = plt.figure(1, figsize=(20,6), dpi=90)
ax = fig.add_subplot(111)


# Title (ground floor)
ar.text(3, 12, "Erdgeschoss", 20)

# outer walls of house
ar.wall(owt, 0, houseWidth-owt, owt, "ground_w1")
ar.wall(owt, houseHeight-owt, houseWidth-owt, houseHeight, "ground_w2")
ar.wall(0, 0, owt, houseHeight, "ground_w3")
ar.wall(houseWidth-owt, 0, houseWidth, houseHeight, "ground_w4")
ar.difference((0.8, 0, 0), (5.2, owt, 2.25), "garageDoor", "ground_w1")  # garage door
ar.difference((6.5, 0, 0), (7.7, owt, 2.1), "mainEntrance", "ground_w1")  # main house entrance door
ar.difference((8.4, 0, 1.2), (9.4, owt, 2.0), "window1", "ground_w1")  # window 1
ar.difference((12.0, 0, 1.2), (13.0, owt, 2.0), "window2", "ground_w1")  # window 2

# garage 
garageWidth = 5.0
ar.wall(garageWidth+owt, owt, garageWidth+owt+iwt, houseHeight-owt)
ar.text(2.0, 3.0, "Garage", roomFontSize)

# room right bottom (room 1)
room1Width = 3.5
room1Height = 3.0
r1_x = houseWidth - owt - room1Width - iwt
r1_y = room1Height + owt + iwt
ar.wall(r1_x, owt, r1_x + iwt, r1_y)
ar.wall(r1_x, r1_y - iwt, houseWidth, r1_y)
ar.text(r1_x + 1.0, r1_y - 2.0, "Zi 1", roomFontSize)

# room2 in ground floor
room2Width = 3.5
room2Height = 3.0
r2_x = houseWidth - owt - room2Width - iwt
r2_y = r1_y + iwt + room2Height
ar.wall(r2_x, r1_y, r2_x + iwt, r2_y)
ar.wall(r2_x, r2_y - iwt, houseWidth, r2_y)
ar.text(r2_x + 1.0, r2_y - 2.0, "Zi 2", roomFontSize)

# room3 in ground floor
room3Width = 3.5
room3Height = 2.5
r3_x = houseWidth - owt - room3Width - iwt
r3_y = r2_y + iwt + room3Height
ar.wall(r3_x, r2_y, r3_x + iwt, r3_y)
ar.wall(r3_x, r3_y - iwt, houseWidth, r3_y)
ar.text(r3_x + 1.0, r3_y - 2.0, "Zi 3", roomFontSize)

# stairs
stairDepth = 0.27
stairWidth = 1.12
stairHeight = 0.185
stairsX = houseWidth - owt - iwt - room1Width - 2 * stairWidth
stairsX = stairsX + 1.2
stairsY = 5.0
ar.drawStairs(stairsX, stairsY - stairDepth * 8, 'v', 8, stairWidth, stairDepth, stairHeight)
ar.drawStairs(stairsX - stairDepth * 8, stairsY, 'h', 7, stairWidth, stairDepth, stairHeight)
ar.line(stairsX+stairWidth, stairsY, stairsX+stairWidth, stairsY+stairWidth)
ar.line(stairsX, stairsY+stairWidth, stairsX+stairWidth, stairsY+stairWidth)


# bottom of ground floor
ar.mf.quad("base", (0, 0, -0.4), (houseWidth, houseHeight, 0))

# bounding box of lower part of house
ar.mf.quad("houseBoundingBox", (0.0, 0.0, -0.4), (houseWidth, houseHeight, 5.0), (1, 1, 0.0))
ar.mf.setVisible("houseBoundingBox", False)
ar.mf.quad("Vorplatz", (0.0, -8, 0.0), (houseWidth, 1.0, 5.0), (1, 1, 0.0))
ar.mf.setVisible("Vorplatz", False)

# mesure lines

xAcc = 0
ar.measureLine(0, -2, 'h', 14, 0.2)
ar.measureLine(xAcc, -1, 'h', owt, 0.2)
xAcc = xAcc + owt
ar.measureLine(xAcc, -1, 'h', garageWidth, 0.2)
xAcc = xAcc + garageWidth
ar.measureLine(xAcc, -1, 'h', iwt, 0.2)
xAcc = xAcc + iwt
stairWayWidth = houseWidth - (2*owt+garageWidth+2*iwt+room1Width)
ar.measureLine(xAcc, -1, 'h', stairWayWidth, 0.2)
xAcc = xAcc + stairWayWidth
ar.measureLine(xAcc, -1, 'h', iwt, 0.2)
xAcc = xAcc + iwt
ar.measureLine(xAcc, -1, 'h', room1Width, 0.2)
xAcc = xAcc + room1Width
ar.measureLine(xAcc, -1, 'h', owt, 0.2)

ar.measureLine(-1.0, 0, 'v', 10, 0.2)

#patch = None
#if (type(polygon) == Polygon):
#    patch = PolygonPatch(polygon, facecolor='#DDDDDD', edgecolor='#000000', alpha=1.0, zorder=2)
#    ax.add_patch(patch)
#else:
#    for p in polygon:
#        patch = PolygonPatch(p, facecolor='#DDDDDD', edgecolor='#000000', alpha=1.0, zorder=2)
#        ax.add_patch(patch)

ar.pltPolygon(ar.polygon)

xrange = [-1, 300]
yrange = [-1, 200]
ax.set_xlim(*xrange)
#ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(*yrange)
#ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)

plt.show()

ar.savePolygonAsSVG(ar.polygon)

ar.svgFile.closeFile()

####################################################################
### FIRST FLOOR AND ROOF ###########################################
####################################################################

ar.etage = 1

fig = plt.figure(2, figsize=(20,6), dpi=90)
ax = fig.add_subplot(111)

polygon = None

ar.initSvgFile("generatedFiles/plan_firstFloor.svg")

# Title (first floor)
ar.text(3, 12, "Erster Stock", 20)


# outer walls of house
brown = (0.95, 0.4, 0.13)
ar.wall(owt, 0, houseWidth-owt, owt, name="first_w1", color=brown)
ar.difference((0.8, 0, 0), (3.8, owt, 2.25), "terrasseDoorSouth", "first_w1")  # terrasseDoorSouth
ar.difference((6.5, 0, 1.0), (7.3, owt, 2.0), "window3", "first_w1")  # window 3
ar.difference((8.4, 0, 1.0), (9.2, owt, 2.0), "window4", "first_w1")  # window 4
ar.difference((12.0, 0, 1.0), (12.8, owt, 2.0), "window5", "first_w1")  # window 5
ar.wall(owt, houseHeight-owt, houseWidth-owt, houseHeight, name="first_w2", color=brown)
ar.wall(0, 0, owt, houseHeight, name="first_w3", color=brown)
ar.difference((0, 1.0, 0), (owt, 4.0, 2.25), "terrasseDoorWest", "first_w3")  # terrasseDoorWest
ar.difference((0, 7.4, 1.0), (owt, 9.0, 2.25), "window6", "first_w3")  # window 6
ar.wall(houseWidth-owt, 0, houseWidth, houseHeight, name="first_w4", color=brown)


# stairs
ar.drawStairs(stairsX, stairsY - stairDepth * 8, 'v', 8, stairWidth, stairDepth, stairHeight)
ar.drawStairs(stairsX - stairDepth * 8, stairsY, 'h', 7, stairWidth, stairDepth, stairHeight)
ar.line(stairsX+stairWidth, stairsY, stairsX+stairWidth, stairsY+stairWidth)
ar.line(stairsX, stairsY+stairWidth, stairsX+stairWidth, stairsY+stairWidth)

ar.wall(garageWidth+owt, owt, garageWidth+owt+iwt, houseHeight-owt, name="wallWZ", color=brown)
ar.difference((garageWidth+owt, 4.0, 0.0), (garageWidth+owt+iwt, 6-0, 2.0), "doorLivingRoom", "wallWZ")  # doorLivingRoom
ar.text(3.0, 3.0, "Wohnzimmer", roomFontSize)

ar.mf.quad("baseFirstFloor", (0, 0, ar.wallHeight), (houseWidth, houseHeight, ar.etageHeight))
ar.difference((garageWidth+owt*2+1.0, 4.9, -1.0), (garageWidth+owt*2+4.0, 6.1, 1.0), "stairsHole", "baseFirstFloor")  # hole for stairs in floor of first floor

# Balkon
ar.mf.quad("Balkon", (0, -2, ar.wallHeight), (4, 0, ar.etageHeight))

# Terrasse
ar.mf.quad("Terrasse", (-4, -2, 0), (0, 10, ar.etageHeight))

### ROOF

ar.mf.quad("roofBase", (0, 0, (ar.etageHeight + ar.wallHeight)), (houseWidth, houseHeight, ar.etageHeight * 2), color=brown)
ptsRF = list()
ofsX = 0.5
ofsY = 0.5
roofStartHeight = ar.etageHeight * 2
roofHeight = 2.0
ptsRF.append((-ofsX, -ofsY, roofStartHeight))
ptsRF.append((ofsX + houseWidth, -ofsY, roofStartHeight))
ptsRF.append((ofsX + houseWidth, houseHeight * 0.5, roofStartHeight))
ptsRF.append((-ofsX, houseHeight * 0.5, roofStartHeight))
ptsRF.append((-ofsX, -ofsY, roofStartHeight+0.1))
ptsRF.append((ofsX + houseWidth, -ofsY, roofStartHeight+0.1))
ptsRF.append((ofsX + houseWidth, houseHeight * 0.5, roofStartHeight+roofHeight))
ptsRF.append((-ofsX, houseHeight * 0.5, roofStartHeight+roofHeight))
ar.mf.deformedQuad("roofFront", ptsRF, (1, 0, 0))

ptsRB = list()
ptsRB.append((-ofsX, houseHeight*0.5, roofStartHeight))
ptsRB.append((ofsX + houseWidth , houseHeight*0.5, roofStartHeight))
ptsRB.append((ofsX + houseWidth, ofsY + houseHeight, roofStartHeight))
ptsRB.append((-ofsX, ofsY + houseHeight, roofStartHeight))
ptsRB.append((-ofsX, houseHeight*0.5, roofStartHeight+roofHeight))
ptsRB.append((ofsX + houseWidth , houseHeight*0.5, roofStartHeight+roofHeight))
ptsRB.append((ofsX + houseWidth, ofsY + houseHeight, roofStartHeight))
ptsRB.append((-ofsX, ofsY + houseHeight, roofStartHeight))
ar.mf.deformedQuad("roofFront", ptsRB, (1, 0, 0))


### Measure Lines

ar.measureLine(0, -2, 'h', 14, 0.2,)
ar.measureLine(0, -1, 'h', owt, 0.2,)
ar.measureLine(owt, -1, 'h', garageWidth, 0.2)
ar.measureLine(owt+garageWidth, -1, 'h', iwt, 0.2)
ar.measureLine(owt+garageWidth+iwt, -1, 'h', 4, 0.2)

ar.measureLine(-1.0, 0, 'v', 10, 0.2)



#patch = None
#if (type(polygon) == Polygon):
#    patch = PolygonPatch(polygon, facecolor='#DDDDDD', edgecolor='#000000', alpha=1.0, zorder=2)
#    ax.add_patch(patch)
#else:
#    for p in polygon:
#        patch = PolygonPatch(p, facecolor='#DDDDDD', edgecolor='#000000', alpha=1.0, zorder=2)
#        ax.add_patch(patch)

ar.pltPolygon(ar.polygon)


xrange = [-1, 300]
yrange = [-1, 200]
ax.set_xlim(*xrange)
#ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(*yrange)
#ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)

plt.show()

ar.savePolygonAsSVG(ar.polygon)

ar.svgFile.closeFile()

ar.mf.closeFile()

####################################################################
####################################################################
####################################################################



