'''
Created on April 11, 2023
Update on Oct. 25, 2023
updated in Feb, 2024 K.

@author: Xu Wang
'''
import os
import argparse
from datetime import datetime
import errno
from exiftool import ExifToolHelper   
import shutil
import numpy

#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-sf", "--srcFolder", required=True, help="source file folder")
ap.add_argument("-ext", "--extType", required=True, help="image extension type")
ap.add_argument("-tf", "--tgtFolder", required=True, help="target file folder")

args = vars(ap.parse_args())
filePath = args["srcFolder"]
print("Source folder is: %s" % filePath)
workingPath = args["tgtFolder"]
print("Target folder is: %s" % workingPath)
exten = args["extType"]

#------------------------------------------------------------------------
# Define the output LogFile
logFile = 'LogCheck_'+datetime.now().strftime("%y%m%d_%H%M%S")+'.txt'
logname = os.path.join(workingPath,logFile)
with open(logname, 'a') as logoutput:
    logoutput.write("File path is: %s\n" % filePath)
print("File path is: %s" % filePath)
#------------------------------------------------------------------------
# Create list of total images
# exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.endswith(exten):
            imList.append(os.path.join(dirpath, name))
with open(logname, 'a') as logoutput:
    logoutput.write("Total images in the path: %d\n" % len(imList))
print("Total images in the path: %d" % len(imList))
#------------------------------------------------------------------------
# Create renamed path
try:
    os.makedirs(workingPath+"\\renamed")
    print("Creating Renamed directory.")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
# Rename and copy into Renamed directory
alti = [] # altitude
with ExifToolHelper() as et:
    for im in imList:
        imObj = im.split("\\")
        numOfObj = len(imObj)
        imFile = imObj[numOfObj-1]
        dtTags = et.get_tags(im, tags=["DateTimeOriginal"])[0]['EXIF:DateTimeOriginal']
        # snTags = str(et.get_tag('EXIF:SerialNumber', im))
        snTags = et.get_tags(im, tags=["Model"])[0]['EXIF:Model']
        dtTags = ''.join(dtTags.split(":")).replace(" ","_")
        tgFile = workingPath+"\\renamed\\"+dtTags+"_"+snTags+"_"+imFile
        newFile = shutil.copy2(im,tgFile)
        print("Copying %s" % newFile)
