#!/bin/sh

python3 bigHouse.py
cd generatedFiles
#blender -P generateCad.py
../../../../blender-2.82a-linux64/blender -P generateCad.py

