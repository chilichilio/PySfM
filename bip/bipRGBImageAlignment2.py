'''
Created on May 9, 2022
Updated on Sep. 6, 2022
Updated on Feb. 15, 2023
updated in Feb, 2024 K.

@author: Xu Wang
'''
import os
import argparse
import Metashape

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-sf", "--srcFolder", required=True, help="source file folder")
ap.add_argument("-ext", "--extType", required=True, help="image extension type")
ap.add_argument("-tf", "--tgtFolder", required=True, help="target file folder")
args = vars(ap.parse_args())
srcImagePath = args["srcFolder"]
print("Source folder is: %s" % srcImagePath)
workingPath = args["tgtFolder"]
print("Target folder is: %s" % workingPath)
imgType = args["extType"]
project = workingPath+"\\ortho_dem_process.psx"


files = os.listdir(srcImagePath+"\\renamed\\")
file_list = []

for file in files:
    print(file)
    if file.endswith(str(imgType)):
        filePath = srcImagePath + "\\renamed\\" + file
        file_list.append(filePath)

app = Metashape.Application()
doc = Metashape.app.document

Metashape.app.gpu_mask = 3
Metashape.app.cpu_enable = True

chunk = Metashape.app.document.addChunk()
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")

doc.save(path=project, chunks=[doc.chunk])

# Import photos
chunk.addPhotos(filenames = file_list)

chunk.matchPhotos(downscale=1, reference_preselection=True, keypoint_limit = 300000, tiepoint_limit = 200000)
# Align photos
chunk.alignCameras(adaptive_fitting=True)
# Save project
doc.save(path=project, chunks=[doc.chunk])
