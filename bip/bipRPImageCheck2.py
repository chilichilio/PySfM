# python bipRPImageCheck2.py F:\
'''
Created on Apr 5, 2018
Updated on Dec 2, 2020
Updated on May 9, 2022
Updated on July 7, 2022
updated in Feb, 2024 K.

@author: Xu Wang
'''
import os
import argparse
from datetime import datetime
import errno
# import exiftool
import shutil
import numpy
from exiftool import ExifToolHelper   
#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("fpath", help="main file path")
args = parser.parse_args()
filePath = args.fpath
#------------------------------------------------------------------------
# Define the output LogFile
logFile = 'LogCheck_'+datetime.now().strftime("%y%m%d_%H%M%S")+'.txt'
logname = os.path.join(filePath,logFile)
with open(logname, 'a') as logoutput:
    logoutput.write("File path is: %s\n" % filePath)
print("File path is: %s" % filePath)
#------------------------------------------------------------------------
# Create list of total images
exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(os.path.join(dirpath, name))
with open(logname, 'a') as logoutput:
    logoutput.write("Total images in the path: %d\n" % len(imList))
print("Total images in the path: %d" % len(imList))
#------------------------------------------------------------------------
# Remove questionable images
# Round I: check image file size
print("R1 check")
r1List=[]
for im in imList:
    fs = os.path.getsize(im)
    if fs > 3000000:
        r1List.append(im)
r2List = []
with ExifToolHelper() as et:
    for im in r1List:
        if et.get_tags(im, tags=["GPSPosition"]) != None:
            r2List.append(im)

# Round II: check completeness
print("R2 check")
imNum = 99999
acc = 0
tempImList=[]
finalImList=[]
questionImList=[]
for im in r2List:
    # Check 1-6
    imObj = im.split("\\")
    numOfObj = len(imObj)
    # Only image file name with no extension
    imNumNext = int(imObj[numOfObj-1].split("_")[1])
    if imNum != imNumNext:
        imNum = imNumNext
        if acc == 6:
            for i in range(0,acc):
                finalImList.append(tempImList[i])
        else:
            for i in range(0,acc):
                questionImList.append(tempImList[i])
        acc = 1
        tempImList.clear()
        tempImList.append(im)
    else:
        acc += 1
        tempImList.append(im)
if acc ==6:
    for i in range(0,6):
        finalImList.append(tempImList[i])
with open(logname, 'a') as logoutput:
    logoutput.write("Total effective images in the path: %d\n" % len(finalImList))
    logoutput.write(''.join(questionImList)+"\n")
print("Total effective images in the path: %d" % len(finalImList))
#------------------------------------------------------------------------
# Create renamed path
try:
    os.makedirs(filePath+"\\renamed")
    print("Creating Renamed directory.")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
# Rename and copy into Renamed directory
alti = [] # altitude
with ExifToolHelper() as et:
    for im in finalImList:
        imObj = im.split("\\")
        numOfObj = len(imObj)
        imFile = imObj[numOfObj-1]
        dtTags = et.get_tags(im, tags=["DateTimeOriginal"])[0]['EXIF:DateTimeOriginal']
        # exifAlti = et.get_tags(im, tags=["GPSAltitude"])['Composite:GPSAltitude']
        exifAlti = et.get_tags(im, tags=["GPSAltitude"])[0]['Composite:GPSAltitude']
        if exifAlti > 0:
            alti.append(exifAlti)
        dtTags = ''.join(dtTags.split(":")).replace(" ","_")
        tgFile = filePath+"\\renamed\\"+dtTags+"_"+imFile
        newFile = shutil.copy2(im,tgFile)
        print("Copying %s" % newFile)
