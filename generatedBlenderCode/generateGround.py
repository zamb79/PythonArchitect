import bpy
import mathutils
from mathutils import Vector


meshName = "ground"
obName = "ground"

me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)

#ob = bpy.data.objects.new(obName)
scn = bpy.context.scene
scn.objects.link(ob)
scn.objects.active = ob
ob.select = True

verts = list()
faces = list()
verts.append((-21.250000, 21.960000, 434.300000))
verts.append((-19.910000, 17.970000, 433.200000))
verts.append((-17.741559, 11.548845, 431.300000))
verts.append((-15.575109, 5.129487, 430.900000))
verts.append((-13.410000, -1.290000, 429.900000))
verts.append((-14.611872, 24.750858, 433.200000))
verts.append((-11.136404, 19.390643, 432.100000))
verts.append((-7.660936, 14.030429, 430.900000))
verts.append((-4.185468, 8.670215, 430.100000))
verts.append((-0.710000, 3.310000, 429.000000))
verts.append((-7.975869, 27.543912, 432.750000))
verts.append((-5.746902, 23.282934, 432.150000))
verts.append((-3.517934, 19.021956, 431.050000))
verts.append((-1.288967, 14.760978, 430.200000))
verts.append((0.940000, 10.500000, 428.950000))
verts.append((-1.340000, 30.340000, 432.300000))
verts.append((1.255000, 26.093750, 432.200000))
verts.append((3.850000, 21.847500, 431.200000))
verts.append((6.445000, 17.601250, 430.300000))
verts.append((9.040000, 13.355000, 428.900000))
verts.append((7.220000, 33.940000, 431.200000))
verts.append((9.700000, 29.507500, 430.500000))
verts.append((12.180000, 25.075000, 430.000000))
verts.append((14.660000, 20.642500, 429.600000))
verts.append((17.140000, 16.210000, 428.500000))
verts.append((15.600000, 37.500000, 429.700000))
verts.append((17.900000, 32.775000, 429.100000))
verts.append((20.200000, 28.050000, 429.000000))
verts.append((22.500000, 23.325000, 428.800000))
verts.append((24.800000, 18.600000, 427.200000))
faces.append((0, 1, 5))
faces.append((1, 6, 5))
faces.append((1, 2, 6))
faces.append((2, 7, 6))
faces.append((2, 3, 7))
faces.append((3, 8, 7))
faces.append((3, 4, 8))
faces.append((4, 9, 8))
faces.append((5, 6, 10))
faces.append((6, 11, 10))
faces.append((6, 7, 11))
faces.append((7, 12, 11))
faces.append((7, 8, 12))
faces.append((8, 13, 12))
faces.append((8, 9, 13))
faces.append((9, 14, 13))
faces.append((10, 11, 15))
faces.append((11, 16, 15))
faces.append((11, 12, 16))
faces.append((12, 17, 16))
faces.append((12, 13, 17))
faces.append((13, 18, 17))
faces.append((13, 14, 18))
faces.append((14, 19, 18))
faces.append((15, 16, 20))
faces.append((16, 21, 20))
faces.append((16, 17, 21))
faces.append((17, 22, 21))
faces.append((17, 18, 22))
faces.append((18, 23, 22))
faces.append((18, 19, 23))
faces.append((19, 24, 23))
faces.append((20, 21, 25))
faces.append((21, 26, 25))
faces.append((21, 22, 26))
faces.append((22, 27, 26))
faces.append((22, 23, 27))
faces.append((23, 28, 27))
faces.append((23, 24, 28))
faces.append((24, 29, 28))

me.from_pydata(verts, [], faces)

bpy.ops.object.mode_set(mode='EDIT')

me.update()

bpy.ops.object.mode_set(mode='OBJECT')
activeObject = bpy.context.active_object #Set active object to variable
mat = bpy.data.materials.new(name="MaterialName") #set new material to
activeObject.data.materials.append(mat) #add the material to the object
bpy.context.object.active_material.diffuse_color = (0.8, 1.0, 0.0) #change color
