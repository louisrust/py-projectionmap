import cv2
import numpy as np

def processImage():
    img = cv2.imread("output-close/rectangle-phase0.jpg")
    sobelx64f = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=1)
    abs_sobel64f = np.absolute(sobelx64f)
    sobel_8u = np.uint8(abs_sobel64f)
    cv2.imshow('sobel',sobel_8u)
    cv2.waitKey(0)  
    #closing all open windows  
    cv2.destroyAllWindows()

processImage()