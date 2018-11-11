
import sys
sys.path.append("..")

import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

import svg
import blenderScript
import architecture as ar

# blender for animation:
# Dope sheet, Timeline
# blender shortcuts:
# Strg + Shift + Num0 -> Camera = current viewitems
# I -> Add current view as key frame 

e = 0.001

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

winW = 0.9
winH = 1.1

####################################################################
### CREATE LIGHT #################################################
####################################################################

# lights outside
ar.bs.createLight(4, -20, 20, 0.707, 0, 0, "SUN")
ar.bs.createLight(-10, 5, 10, 0, 0, 0, "POINT")
ar.bs.createLight(24, 5, 10, 0, 0, 0, "POINT")
ar.bs.createLight(7, 20, 10, 0, 0, 0, "POINT")

# lights inside
ar.bs.createLight(3, 5, 2, 0, 0, 0, "POINT") # light in garage
ar.bs.createLight(3, 5, 5.3, 0, 0, 0, "POINT") # light in living room
ar.bs.createLight(8, 2.5, 2, 0, 0, 0, "POINT") # light behind main entrance






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

ar.bs.mesh("ground", groundPts, faces, (0.8, 1.0, 0.0))

# cut out the house from the ground
ar.differenceAndDelete((-4.0 - e, -10.0 - e, 0.0 - e), (houseWidth + e, houseHeight + e, 5.0 + e), "houseBox", "ground")
ar.differenceAndDelete((0.0, 0.0, -0.4), (houseWidth, houseHeight, 0.05), "houseBoxFloor", "ground")


				
####################################################################
### GROUND FLOOR ###################################################
####################################################################

fig = plt.figure(1, figsize=(20,6), dpi=90)
ax = fig.add_subplot(111)


# Title (ground floor)
ar.text(3, 12, "Erdgeschoss", 20)

# outer walls of house
ar.wall(owt, 0, houseWidth-owt, owt, "ground_w1")  # south wall
ar.wall(owt, houseHeight-owt, houseWidth-owt, houseHeight, "ground_w2")  # north wall
ar.wall(0, 0, owt, houseHeight, "ground_w3")  # west wall
ar.wall(houseWidth-owt, 0, houseWidth, houseHeight, "ground_w4")  # east wall
ar.differenceAndDelete((0.8, 0, e), (5.2, owt, 2.25), "garageDoor", "ground_w1", extendAlongAxis = 1)  # garage door
ar.differenceAndDelete((8.4, 0, e), (9.6, owt, 2.1), "mainEntrance", "ground_w1", extendAlongAxis = 1)  # main house entrance door
ar.differenceAndDelete((6.5, 0, 1.0), (6.5+winW, owt, 1.0+winH), "window1", "ground_w1", extendAlongAxis = 1)  # window 1
ar.differenceAndDelete((11.5, 0, 1.0), (11.5+winW, owt, 1.0+winH), "window2", "ground_w1", extendAlongAxis = 1)  # window 2
ar.differenceAndDelete((houseWidth - owt, 1.5, 1.2), (houseWidth, 1.5+winW, 1.0+winH), "window3", "ground_w4", extendAlongAxis = 0)  # window 3
ar.differenceAndDelete((houseWidth - owt, 7.5, 1.2), (houseWidth, 7.5+winW, 1.0+winH), "window4", "ground_w4", extendAlongAxis = 0)  # window 4

# garage 
garageWidth = 5.0
ar.wall(garageWidth+owt, owt, garageWidth+owt+iwt, houseHeight-owt, "garageInnerWall")
ar.differenceAndDelete((owt + garageWidth, 5.0, e), (owt + garageWidth + iwt, 6.0, 2.25), "innerDoorToGarage", "garageInnerWall", extendAlongAxis = 0)  # inner door to garage
ar.text(2.0, 3.0, "Garage", roomFontSize)

# room right bottom (room 1)
room1Width = 3.5
room1Height = 4.0
r1_x = houseWidth - owt - room1Width - iwt
r1_y = room1Height + owt + iwt
ar.wall(r1_x, owt, r1_x + iwt, r1_y, "frontWallRoom1")
ar.wall(r1_x, r1_y - iwt, houseWidth, r1_y)
ar.text(r1_x + 1.0, r1_y - 2.0, "Zi 1", roomFontSize)
ar.differenceAndDelete((owt + garageWidth + iwt + 4.0, 3.0, e), (owt + garageWidth + iwt + 4.0 + iwt, 4.0, 2.25), "doorRoom1", "frontWallRoom1", extendAlongAxis = 0)  # door to room 1

# room2 in ground floor
room2Width = 3.5
room2Height = 5.0
r2_x = houseWidth - owt - room2Width - iwt
r2_y = r1_y + iwt + room2Height
ar.wall(r2_x, r1_y, r2_x + iwt, r2_y, "frontWallRoom2")
ar.wall(r2_x, r2_y - iwt, houseWidth, r2_y)
ar.text(r2_x + 1.0, r2_y - 2.0, "Zi 2", roomFontSize)
ar.differenceAndDelete((owt + garageWidth + iwt + 4.0, 5.0, e), (owt + garageWidth + iwt + 4.0 + iwt, 6.0, 2.25), "doorRoom2",  "frontWallRoom2", extendAlongAxis = 0)  # door to room 2

# room3 in ground floor
ar.wall(owt + garageWidth + iwt, 6.5, owt + garageWidth + iwt + 4.0, 6.5 + iwt, "room3Wall")
ar.differenceAndDelete((owt + garageWidth + iwt + 2.5, 6.5, e), (owt + garageWidth + iwt + 3.5, 6.5 + iwt, 2.25), "doorRoom3", "room3Wall", extendAlongAxis = 1)  # door to room 3

# stairs
stairDepth = 0.27
stairWidth = 1.12
stairHeight = 3.0 / 16.0
stairsX = owt + garageWidth + iwt
stairsY = owt
ar.drawStairs(stairsX, stairsY, 'v', 8, stairWidth, stairDepth, stairHeight)

# bottom of ground floor
ar.bs.quad("base", (0, 0, -0.4), (houseWidth, houseHeight, 0))

# bounding box of lower part of house
#ar.bs.quad("houseBoundingBox", (0.0, 0.0, -0.4), (houseWidth, houseHeight, 5.0), (1, 1, 0.0))
#ar.bs.setVisible("houseBoundingBox", False)
#ar.bs.quad("Vorplatz", (0.0, -8, 0.0), (houseWidth, 1.0, 5.0), (1, 1, 0.0))
#ar.bs.setVisible("Vorplatz", False)

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
plt.close()

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
ar.differenceAndDelete((0.8, 0, 0 + e), (3.8, owt, 2.25), "terrasseDoorSouth", "first_w1", extendAlongAxis = 1)  # terrasseDoorSouth
ar.differenceAndDelete((6.5, 0, 1.0), (6.5+winW, owt, 1.0+winH), "window11", "first_w1", extendAlongAxis = 1)  # window 11
ar.differenceAndDelete((8.55, 0, 1.0), (8.55+winW, owt, 1.0+winH), "window12", "first_w1" , extendAlongAxis = 1)  # window 12
ar.differenceAndDelete((11.5, 0, 1.0), (11.5+winW, owt, 1.0+winH), "window13", "first_w1", extendAlongAxis = 1)  # window 13
ar.wall(0, 0, owt, houseHeight, name="first_w3", color=brown)
ar.differenceAndDelete((0, 1.0, 0+e), (owt, 4.0, 2.25), "terrasseDoorWest", "first_w3", extendAlongAxis = 0)  # terrasseDoorWest
ar.differenceAndDelete((0, 7.4, 1.0), (owt, 7.4+winW, 1.0+winH), "window14", "first_w3", extendAlongAxis = 0)  # window 14: from kitchen to garden
ar.differenceAndDelete((0, 5.6, 1.0), (owt, 5.6+winW, 1.0+winH), "window15", "first_w3", extendAlongAxis = 0)  # window 15: from living room to garden
ar.wall(houseWidth-owt, 0, houseWidth, houseHeight, name="first_w4", color=brown)
ar.differenceAndDelete((houseWidth - owt, 1.5, 1.0), (houseWidth, 1.5+winW, 1.0+winH), "window16", "first_w4", extendAlongAxis = 0)  # window 16
ar.differenceAndDelete((houseWidth - owt, 4.3, 1.0), (houseWidth, 4.3+winW, 1.0+winH), "window17", "first_w4", extendAlongAxis = 0)  # window 17
ar.differenceAndDelete((houseWidth - owt, 7.5, 1.0), (houseWidth, 7.5+winW, 1.0+winH), "window18", "first_w4", extendAlongAxis = 0)  # window 18
ar.wall(owt, houseHeight-owt, houseWidth-owt, houseHeight, name="first_w2", color=brown) # backside wall
ar.differenceAndDelete((3.0, houseHeight-owt, 1.0), (3.0+winW, houseHeight, 1.0+winH), "window19", "first_w2", extendAlongAxis = 1)  # window 19
ar.differenceAndDelete((6.0, houseHeight-owt, 1.6), (6.0+winW, houseHeight, 1.0+winH), "window20", "first_w2", extendAlongAxis = 1)  # window 20
ar.differenceAndDelete((9.0, houseHeight-owt, 1.0), (9.0+winW, houseHeight, 1.0+winH), "window21", "first_w2", extendAlongAxis = 1)  # window 21
ar.differenceAndDelete((12.0, houseHeight-owt, 1.0), (12.0+winW, houseHeight, 1.0+winH), "window22", "first_w2", extendAlongAxis = 1)  # window 22


# rooms 4 and 7 (in the south of first floor)
ofsFromStair = stairWidth + 0.2
room7_leftX = owt + garageWidth + iwt + ofsFromStair
room7_Width = 3.0
room7_Height = 4.2
room7_stair_edge = 0.6
ar.wall(room7_leftX, room7_Height, houseWidth-owt, room7_Height - iwt, "room7and4Wall")  # top wall of rooms 4 and 7
ar.wall(room7_leftX + room7_Width, owt, room7_leftX + room7_Width + iwt, room7_Height, "firstWall_2")  # wall between rooms 4 and 7
ar.text(room7_leftX + 1.0, 2.0, "Zi 7", roomFontSize)
ar.text(houseWidth - 2.0, 2.0, "Zi 4", roomFontSize)
ar.wall(room7_leftX, owt+stairWidth, room7_leftX + iwt, room7_Height, "room7Wall_1")
ar.wall(room7_leftX + iwt, owt+stairWidth, room7_leftX + iwt + room7_stair_edge, owt+stairWidth+iwt, "room7Wall_2")
ar.wall(room7_leftX + room7_stair_edge, owt, room7_leftX + iwt + room7_stair_edge, owt+stairWidth+iwt, "room7Wall_3")
ar.differenceAndDelete((owt+garageWidth+iwt+3, room7_Height-iwt-e, 0.0 + e), (owt+garageWidth+iwt+3.9, room7_Height+e, 2.0 + e), "door7", "room7and4Wall", extendAlongAxis=0)  # door
ar.differenceAndDelete((owt+garageWidth+iwt+6, room7_Height-iwt-e, 0.0 + e), (owt+garageWidth+iwt+6.9, room7_Height+e, 2.0 + e), "door4", "room7and4Wall", extendAlongAxis=0)  # door


# toilet in first floor
toiletHeight = 2.5
toiletWidth = 1.8
ar.wallStartSize(owt+garageWidth+iwt, houseHeight-owt-toiletHeight, toiletWidth, iwt, "toiletWall")
ar.differenceAndDelete((owt+garageWidth+iwt+0.2, houseHeight-owt-toiletHeight-e, 0.0 + e), (owt+garageWidth+iwt+0.9, houseHeight-owt-toiletHeight+iwt+e, 2.0 + e), "doorToilet", "toiletWall", extendAlongAxis=0)  # doorLivingRoom
ar.text(owt+garageWidth + 1.0, houseHeight-owt-1.0, "WC", roomFontSize)


# rooms 5 and 6 in first floor
leftRoom6 = owt+garageWidth+iwt+toiletWidth
leftRoom5 = leftRoom6 + 3.0
y = room7_Height + 1.2
h = houseHeight - owt - y
ar.wallStartSize(leftRoom6, y, houseWidth - leftRoom6 - owt, iwt, "wallRooms56")
ar.wallStartSize(leftRoom6, y, iwt, h)
ar.wallStartSize(leftRoom5, y, iwt, h)
ar.differenceAndDelete((owt+garageWidth+iwt+3, y-e, 0.0 + e), (owt+garageWidth+iwt+3.9, y+iwt+e, 2.0 + e), "door5", "wallRooms56", extendAlongAxis=0)  # door
ar.differenceAndDelete((owt+garageWidth+iwt+6, y-e, 0.0 + e), (owt+garageWidth+iwt+6.9, y+iwt+e, 2.0 + e), "door6", "wallRooms56", extendAlongAxis=0)  # door


# stairs
#ar.drawStairs(stairsX, stairsY - stairDepth * 8, 'v', 8, stairWidth, stairDepth, stairHeight)
#ar.drawStairs(stairsX - stairDepth * 8, stairsY, 'h', 7, stairWidth, stairDepth, stairHeight)
#ar.line(stairsX+stairWidth, stairsY, stairsX+stairWidth, stairsY+stairWidth)
#ar.line(stairsX, stairsY+stairWidth, stairsX+stairWidth, stairsY+stairWidth)

ar.wall(garageWidth+owt, owt, garageWidth+owt+iwt, houseHeight-owt, name="wallWZ", color=brown)  # wall between stairs and living room
ar.differenceAndDelete((garageWidth+owt, 4.0, 0.0 + e), (garageWidth+owt+iwt, 6-0, 2.0), "doorLivingRoom", "wallWZ", extendAlongAxis=0)  # doorLivingRoom
ar.text(3.0, 3.0, "Wohnzimmer", roomFontSize)

ar.bs.quad("baseFirstFloor", (0, 0, ar.wallHeight), (houseWidth, houseHeight, ar.etageHeight))
ar.differenceAndDelete((garageWidth+owt+iwt, owt, -1.0), (garageWidth+owt+iwt+stairWidth, owt+stairWidth+stairDepth*10, 1.0), "stairsHole", "baseFirstFloor")  # hole for stairs in floor of first floor

# Balkon
ar.bs.quad("Balkon", (0, -2, ar.wallHeight), (4, 0, ar.etageHeight))

# Terrasse
ar.bs.quad("Terrasse", (-4, -2, 0), (0, 10, ar.etageHeight))

### ROOF

ar.bs.quad("roofBase", (0, 0, (ar.etageHeight + ar.wallHeight)), (houseWidth, houseHeight, ar.etageHeight * 2), color=brown)
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
ar.bs.deformedQuad("roofFront", ptsRF, (1, 0, 0))

ptsRB = list()
ptsRB.append((-ofsX, houseHeight*0.5, roofStartHeight))
ptsRB.append((ofsX + houseWidth , houseHeight*0.5, roofStartHeight))
ptsRB.append((ofsX + houseWidth, ofsY + houseHeight, roofStartHeight))
ptsRB.append((-ofsX, ofsY + houseHeight, roofStartHeight))
ptsRB.append((-ofsX, houseHeight*0.5, roofStartHeight+roofHeight))
ptsRB.append((ofsX + houseWidth , houseHeight*0.5, roofStartHeight+roofHeight))
ptsRB.append((ofsX + houseWidth, ofsY + houseHeight, roofStartHeight))
ptsRB.append((-ofsX, ofsY + houseHeight, roofStartHeight))
ar.bs.deformedQuad("roofBack", ptsRB, (1, 0, 0))


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

ar.bs.closeFile()

####################################################################
####################################################################
### ANIMATION
####################################################################

anim = blenderScript.BlenderScript()

anim.openFile("generatedFiles/generateAnimation.py")

framesPerPose = 25
explodeStart = 100
explodeEnd = 150
anim.createKeyFrame( 1, 41.97, -27.51, 39.46, 49.5, 0.654, 48.8)
anim.createKeyFrame( framesPerPose * 1, 30.4, -18.7, 9.8, 76.8, 0.8, 49.1)
anim.createKeyFrame( framesPerPose * 2, 3.7, -29.9, 11.9, 75.6, 0.8, 0)
anim.createKeyFrame( framesPerPose * 3, -20.9, -21.3, 12.8, 71.9, 0.79, -42.4)
anim.createKeyFrame( framesPerPose * 4, -24.1, 2.6, 9.3, 76.4, 0.802, -86)
anim.createKeyFrame( framesPerPose * 5, -19.5, 30.6, 16.2, 69.1, 0.77, -134)
anim.createKeyFrame( framesPerPose * 6, 7.59, 40.2, 17.8, 67.5, 0.768, -183)
anim.createKeyFrame( framesPerPose * 7, 37.55, 22.77, 14.5, 71.1, 0.785, -238)
anim.createKeyFrame( framesPerPose * 8, 36.5, -10.33, 1.01, 93.2, 0.827, -297)
anim.createKeyFrame( framesPerPose * 9, 41.97, -27.51, 39.46, 49.5, 0.654, -312)
anim.createKeyFrame( framesPerPose * 10-1, 7.2, -7.3, 33.6, 21, 0.44, -360.275)
anim.createKeyFrame( framesPerPose * 10  , 7.2, -7.3, 33.6, 21, 0.44,   -0.275)
anim.createKeyFrame( framesPerPose * 14, 7.54, -14.8, 18.8, 48.7, 0.626, 2.64)

# explode roof
anim.createKeyFrame(framesPerPose * 9, 0, 0, 0, 0, 0, 0, "roofFront")
anim.createKeyFrame(framesPerPose * 9, 0, 0, 0, 0, 0, 0, "roofBack")
anim.createKeyFrame(framesPerPose * 9, 0, 0, 0, 0, 0, 0, "roofBase")
anim.createKeyFrame(framesPerPose * 10, 20, 0, 0, 0, 0, 0, "roofFront")
anim.createKeyFrame(framesPerPose * 10, -20, 0, 0, 0, 0, 0, "roofBack")
anim.createKeyFrame(framesPerPose * 10, 0, 20, 0, 0, 0, 0, "roofBase")

# explode first floor
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "first_w1")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "first_w2")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "first_w3")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "first_w4")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "room7and4Wall")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "firstWall_2")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "room7Wall_1")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "room7Wall_2")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "room7Wall_3")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "wallRooms56")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "wallWZ")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "room7and4Wall.001")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "wall.002")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "wall.003")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "toiletWall")
anim.createKeyFrame(framesPerPose * 11, 0, 0, 0, 0, 0, 0, "baseFirstFloor")


anim.createKeyFrame(framesPerPose * 12, 0, -20, 0, 0, 0, 0, "first_w1")
anim.createKeyFrame(framesPerPose * 12, 0, 20, 0, 0, 0, 0, "first_w2")
anim.createKeyFrame(framesPerPose * 12, -20, 0, 0, 0, 0, 0, "first_w3")
anim.createKeyFrame(framesPerPose * 12, 20, 0, 0, 0, 0, 0, "first_w4")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "room7and4Wall")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "firstWall_2")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "room7Wall_1")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "room7Wall_2")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "room7Wall_3")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "wallRooms56")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "wallWZ")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "room7and4Wall.001")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "wall.002")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "wall.003")
anim.createKeyFrame(framesPerPose * 12, 0, 0, 10, 0, 0, 0, "toiletWall")
anim.createKeyFrame(framesPerPose * 12, -20, 0, 0, 0, 0, 0, "baseFirstFloor")


# remove ground front wall
anim.createKeyFrame(framesPerPose * 13, 0, 0, 0, 0, 0, 0, "ground_w1")
anim.createKeyFrame(framesPerPose * 14, -20, 0, 0, 0, 0, 0, "ground_w1")



anim.closeFile()

####################################################################
####################################################################
####################################################################



