


headStr = """import bpy
import mathutils
from mathutils import Vector

# convenince function for removing all objects
def removeAll():
    for o in bpy.data.objects:
        if o.type == 'MESH':
            o.select = True
        else:
            o.select = False

    # call the operator once
    bpy.ops.object.delete()

removeAll()

"""

quadStr = """
meshName = "houseMesh"
obName = "houseOb"

me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)

ob = bpy.data.objects.new(obName)
scn = bpy.context.scene
scn.objects.link(ob)
scn.objects.active = ob
ob.select = True



verts = [(0.0, 0.0, 0.0), (10.0, 3.0, 0.0), (10.0, 3.0, 2.0)]
edges = [(0, 1), (1, 2)]
#faces = [(0, 1, 2)]

me.from_pydata(verts, [], faces)

bpy.ops.object.mode_set(mode='EDIT')

me.update()

bpy.ops.object.mode_set(mode='OBJECT')
"""

meshStartStr = """
meshName = "{:s}"
obName = "{:s}"

me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)

#ob = bpy.data.objects.new(obName)
scn = bpy.context.scene
scn.objects.link(ob)
scn.objects.active = ob
ob.select = True

verts = list()
faces = list()
"""

meshEndStr = """
me.from_pydata(verts, [], faces)

bpy.ops.object.mode_set(mode='EDIT')

me.update()

bpy.ops.object.mode_set(mode='OBJECT')
"""



class MeshFile:
    
    file = None
    
    def openFile(self, fileName):
        self.file = open(fileName, "wt")
        self.file.write(headStr)
        
    def closeFile(self):
        self.file.close()

    def createMeshStr(self, name, pts, faces, color = (0.5, 0.5, 0.5)):
        outStr = ""
        outStr = outStr + meshStartStr.format(name, name)
        #print("faces: "+ str(len(faces)))
        for v in pts:
            #print(str(v))
            outStr = outStr + "verts.append(({:f}, {:f}, {:f}))\n".format(float(v[0]), float(v[1]), float(v[2]))
        for f in faces:
            #print(str(f))
            outStr = outStr + "faces.append(({:d}, {:d}, {:d}))\n".format(int(f[0]), int(f[1]), int(f[2]))                
        outStr = outStr + meshEndStr
		
        outStr = outStr + "activeObject = bpy.context.active_object #Set active object to variable\n"
        outStr = outStr + "mat = bpy.data.materials.new(name=\"MaterialName\") #set new material to\n"
        outStr = outStr + "activeObject.data.materials.append(mat) #add the material to the object\n"
        outStr = outStr + "bpy.context.object.active_material.diffuse_color = (" + str(color[0]) +  ", " + str(color[1]) +  ", " + str(color[2]) +  ") #change color\n"
        #outStr = outStr + "bpy.context.object.mat.diffuse_color = (" + str(color[0]) +  ", " + str(color[1]) +  ", " + str(color[2]) +  ") #change color\n"
        return outStr

    def mesh(self, name, pts, faces, color = (0.5, 0.5, 0.5)):
        self.file.write(self.createMeshStr(name, pts, faces, color))
        
    def quad(self, name, pt1, pt2, color = (0.5, 0.5, 0.5)):
        pts = list()
        pts.append((pt1[0], pt1[1], pt1[2]))
        pts.append((pt2[0], pt1[1], pt1[2]))
        pts.append((pt2[0], pt2[1], pt1[2]))
        pts.append((pt1[0], pt2[1], pt1[2]))
        pts.append((pt1[0], pt1[1], pt2[2]))
        pts.append((pt2[0], pt1[1], pt2[2]))
        pts.append((pt2[0], pt2[1], pt2[2]))
        pts.append((pt1[0], pt2[1], pt2[2]))
        faces = list()
        faces.append((0, 2, 1))
        faces.append((0, 3, 2))
        faces.append((0, 5, 4))
        faces.append((0, 1, 5))
        faces.append((3, 7, 6))
        faces.append((3, 6, 2))
        faces.append((4, 6, 7))
        faces.append((4, 5, 6))
        faces.append((1, 6, 5))
        faces.append((1, 2, 6))
        faces.append((0, 4, 7))
        faces.append((0, 7, 3))
        self.mesh(name, pts, faces, color)

    def deformedQuad(self, name, pts, color = (0.5, 0.5, 0.5)):
        faces = list()
        faces.append((0, 2, 1))
        faces.append((0, 3, 2))
        faces.append((0, 5, 4))
        faces.append((0, 1, 5))
        faces.append((3, 7, 6))
        faces.append((3, 6, 2))
        faces.append((4, 6, 7))
        faces.append((4, 5, 6))
        faces.append((1, 6, 5))
        faces.append((1, 2, 6))
        faces.append((0, 4, 7))
        faces.append((0, 7, 3))
        self.mesh(name, pts, faces, color)

    def setVisible(self, objName, visibleState):
        self.file.write("objects = bpy.data.objects\n")
        self.file.write("objects[\"" + objName + "\"].hide = " + str(not visibleState) + "\n")

    def difference(self, pt1, pt2, diffName, surroundingObjectName):
        self.quad(diffName, pt1, pt2, (0, 1, 0))
        outStr = "\n"
        outStr = outStr + "objects = bpy.data.objects\n"
        outStr = outStr + diffName + "_diffOp = objects[\'" + surroundingObjectName + "\'].modifiers.new(type=\"BOOLEAN\", name=\"" + diffName + "_diffOp\")\n"
        outStr = outStr + diffName + "_diffOp.object = objects[\'" + diffName + "\']\n"
        outStr = outStr + diffName + "_diffOp.operation = \'DIFFERENCE\'\n"
        outStr = outStr + "objects[\'" + diffName + "\'].hide = True\n"
        outStr = outStr + "bpy.context.scene.objects.active = bpy.data.objects[\"" + surroundingObjectName + "\"]\n"
        outStr = outStr + "bpy.ops.object.modifier_apply(modifier=\"" + diffName + "_diffOp\")\n"
        self.file.write(outStr)

