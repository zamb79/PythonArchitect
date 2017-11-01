
import math
from scipy import misc

headerStr = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="1052.3622"
   height="744.09448"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.4 r9939"
   sodipodi:docname="New document 1">
  <defs
     id="defs4" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="1"
     inkscape:cx="20"
     inkscape:cy="20"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     showgrid="false"
     inkscape:window-width="1000mm"
     inkscape:window-height="1000mm"
     inkscape:window-x="400"
     inkscape:window-y="400"
     inkscape:window-maximized="0" />
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">"""

tailStr = """
  </g>
</svg>
"""

def strip(s):
    if (s == ""):
        return s
    if (s[len(s)-1] == '\n'):
        return s[0:len(s)-1]
    return s
    


##############################################################
### Class
##############################################################

class SVG:

    file = None
    
    def openFile(self, fileName):
        self.file = open(fileName, "wt")
        self.file.write(headerStr)

    def closeFile(self):
        self.file.write(tailStr)
        self.file.close()

    def writeText(self, txt, x_orig, y_orig, alpha = 0, fontSize = 9, bold = False):
        alpha = alpha / 180.0 * math.pi
        a0 =  math.cos(alpha)
        a1 =  math.sin(alpha)
        a2 = -math.sin(alpha)
        a3 =  math.cos(alpha)
        x = x_orig * a0 + y_orig * a1
        y = x_orig * a2 + y_orig * a3
        boldStr = "normal"
        if (bold):
            boldStr = "bold"
        textStr = """
        <text
           text-anchor="middle"
           alignment-baseline="central"
           xml:space="preserve"
           style="font-size:""" + str(fontSize) +  """px;font-style:normal;font-weight:""" + boldStr + """;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans"
           x=""" + "\"" + str(x) + "\"" + """
           y=""" + "\"" + str(y) + "\"" + """
           id="text2989"
           sodipodi:linespacing="125%"
           transform="matrix(""" + str(a0) + "," + str(a1) + "," + str(a2) + "," + str(a3) + "," + """0,0)"><tspan
             sodipodi:role="line"
             id="tspan2991"
             x=""" + "\"" + str(x) + "\"" + """
             y=""" + "\"" + str(y) + "\"" + """
             style="font-size:""" + str(fontSize) + """px;font-style:normal;font-variant:normal;font-weight:""" + boldStr + """;font-stretch:normal;font-family:Comic Sans MS;-inkscape-font-specification:Comic Sans MS">""" + txt + """</tspan></text>\n"""
        self.file.write(textStr)
    
    def writeRect(self, x, y, w, h, fill="none"):
        rectStr = """
        <rect
           style="fill:""" + fill + """;stroke:#000000;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0"
           id="rect2987"
           width=""" + "\"" + str(w) + "\"" + """
           height=""" + "\"" + str(h) + "\"" + """
           x=""" + "\"" + str(x) + "\"" + """
           y=""" + "\"" + str(y) + "\"" + """ />\n"""
        self.file.write(rectStr)
        
    def writePolygon(self, points):
        polyStr = """
        <path
           style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
           d="M """ 
        for i in range(0, int(len(points) / 2)):
            polyStr = polyStr + str(points[i*2+0]) + ", " + str(points[i*2+1]) + " "
        polyStr = polyStr + """"       id="path2988"
           inkscape:connector-curvature="0" />\n"""
        self.file.write(polyStr)
    
    def savePolyXY(self, xy):
        cc = list()
        for i in range(0, len(xy[0])):
            cc.append(xy[0][i])
            cc.append(xy[1][i])
        self.writePolygon(cc)
    
    def writeCirc(self, x, y, r, lineWidth):
        circStr = "<circle cx=\"" + str(x) + "\" cy=\"" + str(y) + "\" r=\"" + str(r) + "\" stroke=\"black\" stroke-width=\"" + str(lineWidth) + "\" fill=\"none\" />"
        self.file.write(circStr)
    
    def writeImage(self, x, y, w, h, imageFileName):
        fn = imageFileName.replace("\\", "/")
        imgStr = "<image y=\"" + str(y) + "\" x=\"" + str(x) + "\" "
        imgStr = imgStr + """id="image""" + str(x) + str(y) + """\"
           xlink:href="file:///""" + fn + "\" \n"
        img = misc.imread(imageFileName)
        if (h < 0):
            h = int((float(w) / float(img.shape[1])) * img.shape[0])
            print(imageFileName + "(" + str(img.shape[0]) + "x" + str(img.shape[1]) + "): w=" + str(w) + " h<0 => h=" + str(h))
        if (w < 0):
            w = int((float(h) / float(img.shape[0])) * img.shape[1])
            print(imageFileName + "(" + str(img.shape[0]) + "x" + str(img.shape[1]) + "): h=" + str(h) + " w<0 => w=" + str(w))
        if (h > 0):
            imgStr = imgStr + "height=\"" + str(h) + "\" \n"
        if (w > 0):
            imgStr = imgStr + "width=\"" + str(w) + "\" \n"
        imgStr = imgStr + "/>\n"
        self.file.write(imgStr)
    
    
##################################################

