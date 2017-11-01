import sys
sys.path.append("../")
import svg
import blenderMesh as bm
import numpy as np

pts = np.genfromtxt('points.csv', delimiter=',')

faces = list()
for i in range(0, 5):
    for j in range(0, 4):
        idx1 = i * 5 + j
        idx2 = i * 5 + j + 1
        idx3 = (i+1) * 5 + j
        idx4 = (i+1) * 5 + j + 1
        faces.append([idx1, idx2, idx3])
        faces.append([idx2, idx4, idx3])

f = bm.MeshFile()
f.openFile("../generatedBlenderCode/generateGround.py")
f.mesh("ground", pts, faces, (0.8, 1.0, 0.0))
f.closeFile()
