import math


headStr = """import bpy
import mathutils
from mathutils import Vector

# convenince function for removing all mesh objects
def removeAllMeshes():
    for o in bpy.data.objects:
        if o.type == 'MESH':
            o.select_set(True)
        else:
            o.select_set(False)

    # call the operator once
    bpy.ops.object.delete()

###removeAllMeshes()

myCol = bpy.data.collections.new("collection")
bpy.context.scene.collection.children.link(myCol)

"""

quadStr = """
meshName = "houseMesh"
obName = "houseOb"

me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)

ob = bpy.data.objects.new(obName)
scn = bpy.context.scene
myCol.objects.link(ob)
bpy.context.view_layer.objects.active = ob
ob.select_set(True)



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
myCol.objects.link(ob)
bpy.context.view_layer.objects.active = ob
ob.select_set(True)

verts = list()
faces = list()
"""

meshEndStr = """
me.from_pydata(verts, [], faces)

bpy.ops.object.mode_set(mode='EDIT')

me.update()

bpy.ops.object.mode_set(mode='OBJECT')
"""

wireframeStartStr = """
meshName = "{:s}"
obName = "{:s}"

me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)

#ob = bpy.data.objects.new(obName)
scn = bpy.context.scene
myCol.objects.link(ob)
bpy.context.view_layer.objects.active = ob
ob.select_set(True)

verts = list()
edges = list()
"""

wireframeEndStr = """
me.from_pydata(verts, edges, [])

bpy.ops.object.mode_set(mode='EDIT')

me.update()

bpy.ops.object.mode_set(mode='OBJECT')
"""


class BlenderScript:
    
    file = None
    
    def __init__(self, fileName):
        self.openFile(fileName)
        
    def __del__(self):
        self.closeFile()
    
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
        #outStr = outStr + "bpy.context.object.active_material.diffuse_color = (" + str(color[0]) +  ", " + str(color[1]) +  ", " + str(color[2]) +  ") #change color\n"
        #outStr = outStr + "bpy.context.object.mat.diffuse_color = (" + str(color[0]) +  ", " + str(color[1]) +  ", " + str(color[2]) +  ") #change color\n"
        return outStr
        
    def createWireframeStr(self, name, pts, edges, color = (0.5, 0.5, 0.5)):
        outStr = ""
        outStr = outStr + wireframeStartStr.format(name, name)
        #print("edges: "+ str(len(edges)))
        for v in pts:
            #print(str(v))
            outStr = outStr + "verts.append(({:f}, {:f}, {:f}))\n".format(float(v[0]), float(v[1]), float(v[2]))
        for e in edges:
            #print(str(f))
            outStr = outStr + "edges.append(({:d}, {:d}))\n".format(int(e[0]), int(e[1]))
        outStr = outStr + wireframeEndStr
		
        outStr = outStr + "activeObject = bpy.context.active_object #Set active object to variable\n"
        outStr = outStr + "mat = bpy.data.materials.new(name=\"MaterialName\") #set new material to\n"
        #outStr = outStr + "activeObject.data.materials.append(mat) #add the material to the object\n"
        #outStr = outStr + "bpy.context.object.active_material.diffuse_color = (" + str(color[0]) +  ", " + str(color[1]) +  ", " + str(color[2]) +  ") #change color\n"
        #outStr = outStr + "bpy.context.object.mat.diffuse_color = (" + str(color[0]) +  ", " + str(color[1]) +  ", " + str(color[2]) +  ") #change color\n"
        return outStr

    def mesh(self, name, pts, faces, color = (0.5, 0.5, 0.5)):
        self.file.write(self.createMeshStr(name, pts, faces, color))
        
    def wireframe(self, name, pts, edges, color = (0.5, 0.5, 0.5)):
        self.file.write(self.createWireframeStr(name, pts, edges, color))
        
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
        self.file.write("objects[\"" + objName + "\"].hide_set(" + str(not visibleState) + ")\n")

    def difference(self, pt1, pt2, diffName, surroundingObjectName):
        self.quad(diffName, pt1, pt2, (0, 1, 0))
        outStr = "\n"
        outStr = outStr + "objects = bpy.data.objects\n"
        outStr = outStr + diffName + "_diffOp = objects[\'" + surroundingObjectName + "\'].modifiers.new(type=\"BOOLEAN\", name=\"" + diffName + "_diffOp\")\n"
        outStr = outStr + diffName + "_diffOp.object = objects[\'" + diffName + "\']\n"
        outStr = outStr + diffName + "_diffOp.operation = \'DIFFERENCE\'\n"
        outStr = outStr + "objects[\'" + diffName + "\'].hide_set(True)\n"
        #outStr = outStr + "bpy.context.scene.objects.active = bpy.data.objects[\"" + surroundingObjectName + "\"]\n"
        outStr = outStr + "bpy.context.view_layer.objects.active = bpy.data.objects[\"" + surroundingObjectName + "\"]\n"
        outStr = outStr + "bpy.ops.object.modifier_apply(modifier=\"" + diffName + "_diffOp\")\n"
        self.file.write(outStr)

    def deleteObject(self, objName):
        self.file.write("\nbpy.ops.object.select_all(action=\'DESELECT\')\n")
        self.file.write("bpy.data.objects[\"" + objName + "\"].select_set(True)\n")
        self.file.write("bpy.ops.object.delete()\n")
        
    def createLight(self, x, y, z, rotX, rotY, rotZ, lightType = "HEMI"):
        self.file.write("\nbpy.ops.object.select_all(action=\"DESELECT\")\n")
        self.file.write("bpy.ops.object.light_add(type=\"" + lightType + "\")\n")
        self.file.write("bpy.context.selected_objects[0].location=({:f}, {:f}, {:f})\n".format(x, y, z))
        self.file.write("bpy.context.selected_objects[0].rotation_euler=({:f}, {:f}, {:f})\n".format(rotX, rotY, rotZ))
        
    def createKeyFrameStr(self, frameNum, x, y, z, rotX, rotY, rotZ, objName = "Camera"):
        pi = math.pi
        keyFrameStr = """
bpy.ops.object.select_all(action=\'DESELECT\')
bpy.data.objects['""" + objName + """'].select_set(True)
bpy.context.scene.frame_set({:d})
bpy.data.objects['""" + objName + """'].rotation_euler[0] = {:f}
bpy.data.objects['""" + objName + """'].rotation_euler[1] = {:f}
bpy.data.objects['""" + objName + """'].rotation_euler[2] = {:f}
bpy.data.objects['""" + objName + """'].location[0] = {:f}
bpy.data.objects['""" + objName + """'].location[1] = {:f}
bpy.data.objects['""" + objName + """'].location[2] = {:f}
bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
"""
        return keyFrameStr.format(frameNum,rotX/180.0*pi, rotY/180.0*pi, rotZ/180.0*pi, x, y, z)
        
    def createKeyFrame(self, frameNum, x, y, z, rotX, rotY, rotZ, objName = "Camera"):
        self.file.write(self.createKeyFrameStr(frameNum, x, y, z, rotX, rotY, rotZ, objName))
        
    def animTest(self):
        self.file.write(self.createKeyFrameStr(0,  6, -30, 1.8, 90,   0, -45))
        self.file.write(self.createKeyFrameStr(10, 6, -20,   3, 90,  -5, -45))
        self.file.write(self.createKeyFrameStr(20, 6, -10,   4, 90, -20, -45))
