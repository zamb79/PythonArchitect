#!/bin/sh

python blockHouse.py
cd generatedFiles
blender -P generateCad.py
