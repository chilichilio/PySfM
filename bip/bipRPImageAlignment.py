'''
Created on May 9, 2022
Updated on July 7, 2022

@author: Xu Wang
'''
import os
import argparse
import Metashape

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
workingPath = args["wpath"]
print("Working path is: %s" % workingPath)
srcImagePath = workingPath
project = workingPath+"\\ortho_dem_process.psx"


files = os.listdir(srcImagePath+"\\renamed\\")
file_list=[]

for file in files:
    if file.endswith(".tif"):
        filePath = srcImagePath +"\\renamed\\"+ file
        file_list.append(filePath)

fileGroups = [6]*(len(file_list)//6)

app = Metashape.Application()
doc = Metashape.app.document

# PhotoScan.app.console.clear()

Metashape.app.gpu_mask = 3
Metashape.app.cpu_enable = True

chunk = Metashape.app.document.addChunk()
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")

doc.save(path=project, chunks=[doc.chunk])


# Import photos
chunk.addPhotos(filenames = file_list, filegroups = fileGroups, layout = Metashape.MultiplaneLayout)

chunk.primary_channel = 2

chunk.locateReflectancePanels()

# Panel info
# RP06-2146445-OB
# albedo = {"Blue": "0.480", "Green": "0.481", "Red": "0.480", "NIR": "0.477", "Red edge": "0.479", "Panchro": "0.479"}

# RP06-2147128-OB
albedo = {"Blue": "0.501", "Green": "0.505", "Red": "0.506", "NIR": "0.505", "Red edge": "0.506", "Panchro": "0.50"}

# albedo = {"Blue": "0.630", "Green": "0.634", "Red": "0.631", "NIR": "0.460", "Red edge": "0.625"}
# albedo = {"Blue": "0.488", "Green": "0.488", "Red": "0.487", "NIR": "0.485", "Red edge": "0.486", "Panchro": "0.487"}
for sensor in chunk.sensors:
    sensor.normalize_sensitivity = True
for camera in chunk.cameras:
    if camera.group and camera.group.label == "Calibration images":
        for plane in camera.planes:
            plane.meta["ReflectancePanel/Calibration"] = albedo[plane.sensor.bands[0]]
chunk.calibrateReflectance(use_reflectance_panels=True, use_sun_sensor=True)
doc.save(path=project, chunks=[doc.chunk])

chunk.matchPhotos(downscale=1, reference_preselection=True, keypoint_limit = 150000, tiepoint_limit = 100000)
# Align photos
chunk.alignCameras(adaptive_fitting=True)
# Save project
doc.save(path=project, chunks=[doc.chunk])
