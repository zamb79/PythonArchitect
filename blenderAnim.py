import math

headStr = """import bpy
import mathutils
import math
from mathutils import Vector

"""

class AnimFile:

    file = None
    
    def openFile(self, fileName):
        self.file = open(fileName, "wt")
        self.file.write(headStr)
        
    def closeFile(self):
        self.file.close()

    def createKeyFrameStr(self, frameNum, x, y, z, rotX, rotY, rotZ):
        pi = math.pi
        keyFrameStr = """
bpy.ops.object.select_all(action=\'DESELECT\')
bpy.data.objects['Camera'].select=True
bpy.context.scene.frame_set({:d})
bpy.data.objects['Camera'].rotation_euler[0] = {:f}
bpy.data.objects['Camera'].rotation_euler[1] = {:f}
bpy.data.objects['Camera'].rotation_euler[2] = {:f}
bpy.data.objects['Camera'].location[0] = {:f}
bpy.data.objects['Camera'].location[1] = {:f}
bpy.data.objects['Camera'].location[2] = {:f}
bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
""".format(frameNum,rotX/180.0*pi, rotY/180.0*pi, rotZ/180.0*pi, x, y, z)
        return keyFrameStr
        
    def createKeyFrame(self, frameNum, x, y, z, rotX, rotY, rotZ):
        self.file.write(self.createKeyFrameStr(frameNum, x, y, z, rotX, rotY, rotZ))
        
    def animTest(self):
        self.file.write(self.createKeyFrameStr(0,  6, -30, 1.8, 90,   0, -45))
        self.file.write(self.createKeyFrameStr(10, 6, -20,   3, 90,  -5, -45))
        self.file.write(self.createKeyFrameStr(20, 6, -10,   4, 90, -20, -45))