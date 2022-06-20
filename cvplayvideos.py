import numpy as np
import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import time
from audioplayer import AudioPlayer

r = [[[421, 650], [194, 649], [168, 365], [408, 338]], [[421, 650], [610, 645], [613, 376], [408, 338]], [[871, 650], [610, 645], [613, 376], [892, 352]], [[871, 650], [942, 645], [961, 372], [892, 352]], [[613, 376], [490, 350], [484, 205], [609, 187]], [[613, 376], [689, 366], [692, 216], [609, 187]]]


sVid = "./media/test.mp4"

sv1 = cv.VideoCapture(sVid)
sv2 = cv.VideoCapture(sVid)
sv3 = cv.VideoCapture(sVid)
sv4 = cv.VideoCapture(sVid)
sv5 = cv.VideoCapture(sVid)
sv6 = cv.VideoCapture(sVid)
#sv3 = cv.VideoCapture("./media/mathsl.mp4")
#sv5 = cv.VideoCapture(0)
#sv4 = cv.VideoCapture("./media/mathsr.mp4")
sources = [sv1,sv2,sv3,sv4,sv5,sv6]

fps = sv1.get(cv.CAP_PROP_FPS)

scrwidth = 1920
scrheight = 1080

player = AudioPlayer("./media/test.mp3")

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

startTime = time.time()
frameGlobal = 1
audioStartTime = time.time()
estAudioFrame = 1
class MainWindow():
    def __init__(self, window, sources):
        self.window = window
        self.sources = sources
        self.width = 1280
        self.height = 720
        self.interval = round(1000/fps) # Interval in ms to get the latest frame
        # Create canvas for image
        self.canvas = tk.Canvas(self.window, bg='black', width=scrwidth, height=scrheight)
        self.canvas.create_rectangle(0,0,1920,1080,fill="black",outline="black")
        self.canvas.grid(row=0, column=0)
        # Update image on canvas
        self.update_image()
        self.window.bind("<Button-1>",self.back5)
        self.window.bind("<Button-2>",self.forward5)
        self.window.bind("<Double 1>",self.catchUp)
    def back5(self,event):
        print("Back 5")
        for s in self.sources:
            s.set(cv.CAP_PROP_POS_FRAMES,s.get(cv.CAP_PROP_POS_FRAMES)-5)
    def forward5(self,event):
        print("Forward 5")
        for s in self.sources:
            s.set(cv.CAP_PROP_POS_FRAMES,s.get(cv.CAP_PROP_POS_FRAMES)+5)
    def catchUp(self,event):
        for s in self.sources:
            s.set(cv.CAP_PROP_POS_FRAMES,estAudioFrame)
        print(f"Video frame: {sv1.get(cv.CAP_PROP_POS_FRAMES)}")
        print(f"Audio estimated frame: {estAudioFrame}")
    def update_image(self):
        global frameGlobal
        global startTime
        global audioStartTime
        global estAudioFrame

        estAudioFrame = round((time.time()-audioStartTime)*fps)
        if (abs(sv1.get(cv.CAP_PROP_POS_FRAMES)-estAudioFrame)>60):
            self.catchUp(0)

        self.window.after(self.interval, self.update_image)
        frameTime = time.time()-startTime
        startTime = time.time()
        self.imagesOut = []
        it = 0
        for s in self.sources:
            sFrame = s.read()[1]
            frameCurrent = s.get(cv.CAP_PROP_POS_FRAMES)
            if (sources[0].get(cv.CAP_PROP_POS_FRAMES)==1):
                player.play(block=False)
                audioStartTime = time.time()
            if frameCurrent == s.get(cv.CAP_PROP_FRAME_COUNT):
                frame_counter = 0 #Or whatever as long as it is the same as next line
                s.set(cv.CAP_PROP_POS_FRAMES, 0)
            frame = cv.cvtColor(sFrame, cv.COLOR_BGR2RGB) # to RGB
            imageOut = warpFrame(frame,640,360,r[it])
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
        frameGlobal +=1

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen',True)
    MainWindow(root, sources)
    root.mainloop()
