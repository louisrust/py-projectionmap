import numpy as np
import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk


#r = [[[86, 289], [206, 286], [222, 669], [107, 678]], [[392, 319], [533, 318], [535, 579], [396, 554]], [[673, 579], [672, 704], [276, 689], [271, 571]]]
r = [[[286, 580], [470, 602], [471, 728], [291, 696]], [[470, 602], [614, 573], [614, 685], [472, 727]], [[287, 579], [436, 554], [613, 572], [471, 602]]]




source1 = cv.VideoCapture("./media/video1.mp4")
source2 = cv.VideoCapture("./media/video2.mp4")
source3 = cv.VideoCapture("./media/video3.mp4")
source4 = cv.VideoCapture("./media/video4.mp4")
sources = [source1,source2,source3]

scrwidth = 1024
scrheight = 768

def warpFrame(img,w,h,p):
    #determine size of new polygon
    xmin = p[0][0]
    ymin = p[0][1]
    xmax = p[0][0]
    ymax = p[0][1]
    for xy in p:
        if (xy[0]<xmin):
            xmin = xy[0]
        if (xy[0]>xmax):
            xmax = xy[0]
        if (xy[1]<ymin):
            ymin = xy[1]
        if (xy[1]>ymax):
            ymax = xy[1]
    polwid = xmax-xmin
    polhei = ymax-ymin

    imgwid = img.shape[1]
    imghei = img.shape[0]

    # translate to top left corner
    T = np.float32([
        [1,0,xmin],
        [0,1,ymin]
    ])

    #resize
    img = cv.resize(img,(polwid,polhei), interpolation = cv.INTER_CUBIC)
    
    #translate
    img = cv.warpAffine(img,T,(imgwid,imghei))

    #perspective
    framepts = np.float32([
        [xmin,ymax],
        [xmax,ymax],
        [xmax,ymin],
        [xmin,ymin]
    ])
    destpts = np.float32(p)
    P = cv.getPerspectiveTransform(framepts,destpts)
    img = cv.warpPerspective(img,P,(imgwid,imghei))

    return img


class MainWindow():
    def __init__(self, window, sources):
        self.window = window
        self.sources = sources
        self.width = 1024
        self.height = 768
        self.interval = 20 # Interval in ms to get the latest frame
        # Create canvas for image
        self.canvas = tk.Canvas(self.window, width=scrwidth, height=scrheight)
        self.canvas.grid(row=0, column=0)
        # Update image on canvas
        self.update_image()
    def update_image(self):
        self.imagesOut = []
        it = 0
        for s in self.sources:
            frame = cv.cvtColor(s.read()[1], cv.COLOR_BGR2RGB) # to RGB
            imageOut = warpFrame(frame,1280,720,r[it])
            self.imagesOut.append(imageOut)
            it += 1

        nOut = len(self.sources)
        if nOut==1:
            self.blendOut = self.imagesOut[0]
        if nOut>1:
            for i in range(nOut):
                if i==0:
                    self.blendOut = self.imagesOut[0]
                else:
                    self.blendOut = cv.add(self.blendOut,self.imagesOut[i])

        self.canvasOut = Image.fromarray(self.blendOut) # to PIL format
        self.canvasOut = ImageTk.PhotoImage(self.canvasOut) # to ImageTk format

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvasOut)
        
        # Repeat every 'interval' ms
        self.window.after(self.interval, self.update_image)
if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen',True)
    MainWindow(root, sources)
    root.mainloop()