#!/bin/sh

python bigHouse.py
cd generatedFiles
blender -P generateCad.py
