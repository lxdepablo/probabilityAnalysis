import cv2
import numpy as np

class Clone:
    def __init__(self, imageName):
        self.imageName = imageName

        #load in image
        img = cv2.imread(imageName)
        #find and store all dark pixels in coords
        h, w, c = img.shape
        #make 2D numpy array of size w*h filled with zeros
        arrayShape = (h, w)
        self.coords = np.zeros(arrayShape)
        x = 0
        while x<w:
            y = 0
            while y<h:
                if img[y,x][0] != 255:
                    self.coords[y,x] = 1
                y+=1
            x+=1
