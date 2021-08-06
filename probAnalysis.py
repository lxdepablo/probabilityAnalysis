import cv2
import numpy as np
import clone
import pix
import os

#find width and height of sample image
img = cv2.imread("HWSample.tif")
h, w, c = img.shape
imageSize = (h, w)
#load in a line and find its coordinates in the image
def getLineCoords(imageName):
    line = cv2.imread(imageName)#load line image
    h, w, c = line.shape#get width and height of img
    #print(w,h)
    x = 0
    lineCoords = []
    while(x<w):
        y = 0
        currPixelVal = [255,255,255]
        while(y<h and currPixelVal[0] == 255):
            currPixelVal = line[y,x]#check grayscale value of each pixel
            y+=1
        if(currPixelVal[0] == 255):#if no dark pixels found recycle last used coord
            if(x == 0):
                lineCoords.insert(x, w/2)
            else:
                lastVal = lineCoords[x-1]
                lineCoords.insert(x, lastVal)
        else:
            lineCoords.insert(x,y-1)#add line coord to list
        x+=1

    return lineCoords


#load in all images
# set working directory to desired masks/input folder
os.chdir("biggerClones")
# put filenames into an array
files = os.listdir()

#make all files into clones and add all clones to all pixels
allClones = np.empty(len(files), dtype = clone.Clone)
for x in range(len(files)):
    #print(x)
    allClones[x] = clone.Clone(files[x])

#make array of pixels
#add all clones to each pixel
#save probability map from each pixel
os.chdir("../")
#allPixels = np.empty((h,w), dtype = pix.Pix)
#x = 0
#while(x<w):
#    y = 0
#    while(y<h):
#        allPixels[y,x] = pix.Pix(x, y, imageSize)
#        for clone in allClones:
#            allPixels[y,x].addClone(clone)
#        thisPix = allPixels[y,x]
#        thisPix.calcProbs()
#        #thisPix.displayImg()
#        if thisPix.probMap[thisPix.y, thisPix.x] > 0:
#            thisPix.saveImage()
#        #allPixels[y,x].calcProbs()
#        y+=1
#    x+=1


#Do line analysis
#Read in line template and create array with its coordinates
line = getLineCoords("randLine.tif")

#get average probability that clones respect compartment boundary
lineProbs = np.empty(len(allClones))
index = 0
for clone in allClones:
    #check percent of pix above line
    sameSide = True
    top = True
    h, w = clone.coords.shape
    cloneSize = 0
    pixAbove = 0
    x = 0
    while x<w:
        y = 0
        while y<h:
            if clone.coords[y,x] == 1:
                cloneSize += 1
                #check if pixel is above line
                if line[x] >= y:
                    pixAbove += 1
            y+=1
        x+=1
    #compute probability and store it in lineProbs
    if cloneSize > 0:
        percent = pixAbove / cloneSize
        #what percent is on one side of line
        if percent >= 0.5:
            lineProbs[index] = percent
            #print(str(index) + ": " + str(percent))
        else:
            lineProbs[index] = 1-percent
    else:
        lineProbs[index] = np.NaN
    index += 1

np.savetxt("randLineProbs.csv", lineProbs, delimiter=",")
#print(lineProbs[292])










#
