import cv2
import numpy as np
from PIL import Image
import os

class Pix:
    def __init__(self, x, y, imageSize):
        self.x = x
        self.y = y
        h, w = imageSize
        self.probMap = np.zeros(imageSize)

    def addClone(self, thisClone):
        #if clone contains this pixel add it
        if thisClone.coords[self.y,self.x] == 1:
            self.probMap = np.add(self.probMap, thisClone.coords)

    def calcProbs(self):
        if(self.probMap[self.y,self.x] != 0):
            print(self.probMap[0,0])
            self.probMap /= self.probMap[self.y,self.x]

    def displayImg(self):
        w, h = self.probMap.shape
        self.probMap[self.y,self.x] = 0;
        dim = (w*10, h*10)
        resized = cv2.resize(self.probMap, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("probMap", resized)
        cv2.waitKey()
        #cv2.imwrite("sample.png", resized)
        img = Image.fromarray(np.uint8(resized*255), 'L')
        #img.show()
        self.probMap[self.y,self.x] = 1;
        #cv2.imwrite("test.png", self.probMap)

    def saveImage(self):
        imgName = "_".join((str(self.x),str(self.y)))
        imgName = imgName + ".png"
        w, h = self.probMap.shape
        self.probMap[self.y,self.x] = 0;
        dim = (h*10, w*10)
        resized = cv2.resize(self.probMap, dim, interpolation = cv2.INTER_AREA)
        img = Image.fromarray(np.uint8(resized*255), 'L')
        os.chdir("output")
        img.save(imgName)
        self.probMap[self.y,self.x] = 0;
        os.chdir("../")
