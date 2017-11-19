
from matplotlib import pyplot as plt
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

import svg
import blenderMesh as bm

svgFile = None
mf = None
polygon = None

startX = 7.0
startY = 5.0

svgHeight = 744.09448
#svgScale = 34.9283765 * 1.048689138 # PDF Version: svgUnits per Meter
svgScale = 34.9283765 # Inkscape version: svgUnits per Meter

roomFontSize = 14

etageHeight = 3.0
wallHeight = 2.6
etageCeilThick = etageHeight - wallHeight
etage = 0

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

def drawStairs(x, y, align, numStairs, stairWidth, stairDepth, stairHeight):
    global mf
    line(x+stairWidth, y+stairWidth, x+stairWidth+stairDepth*4, y+stairWidth)
    line(x+stairWidth, y+stairWidth, x+stairWidth, y+stairWidth+stairDepth*10)
    for i in range(0,5):
        z1 = stairHeight * (float(i)+0.5)
        z2 = stairHeight * (i+1)
        line(x+stairWidth+(stairDepth*(4-i)), y, x+stairWidth+(stairDepth*(4-i)), y+stairWidth)
        mf.quad("stair", (x+stairWidth+(stairDepth*(3-i)), y, z1), (x+stairWidth+(stairDepth*(4-i)), y+stairWidth, z2))
    for i in range(0,11):
        z1 = stairHeight * (float(i)+5.5)
        z2 = stairHeight * (i+6)
        line(x, y+stairWidth+i*stairDepth, x+stairWidth, y+stairWidth+i*stairDepth)
        mf.quad("stair", (x, y+stairWidth+i*stairDepth, z1), (x+stairWidth, y+stairWidth+(i+1)*stairDepth, z2))
    mf.quad("stair", (x, y, stairHeight * 4.5), (x+stairWidth, y+stairWidth, stairHeight * 5))

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

def initSvgFile(fileName):
    global svgFile
    svgFile = svg.SVG()
    svgFile.openFile(fileName)
	
def initMeshFile(fileName):
    global mf
    mf = bm.MeshFile()
    mf.openFile(fileName)
				
####################################################################
### GROUND FLOOR ###################################################
####################################################################



