import tkinter as tk
import time
import cv2
root = tk.Tk()
root.attributes('-fullscreen', True) # make main window full-screen

# initialize the camera
cam = cv2.VideoCapture(0)   # 0 -> index of camera

w = tk.Canvas(root, bg='black', highlightthickness=0,cursor="none")
w.pack(fill=tk.BOTH, expand=True) # configure canvas to occupy the whole main window
it = 0          # to use later
sw = 1024       # window width
sh = 768        # window height
n = 32          # number of lines
phases = 4      # number of times to shift
latency = 1000  # time before starting
delay = 1000    # delay between each shift
width=3         # line width in pixels
def iterateLines():
    global it
    w.create_rectangle(0,0,sw+1,sh,outline="#000",fill="#000")
    lines = []
    for i in range(1,n+1):
        div = sw/n
        lx = ((sw/n)*i)-it*(div/phases) # line x value
        lines.append(w.create_rectangle(lx,0,lx+(width-1),sh,outline="#f00",fill="#f00"))
    it = it+1


outputFolder = "output"
def process():
    s, img = cam.read()
    if s: # success
        #red = img.copy()
        #red[:,:,0] = 0
        #red[:,:,1] = 0
        r = cv2.Canny(img,100,200)
        cv2.imwrite(outputFolder+"/phase"+str(it)+".jpg",img)
        cv2.imwrite(outputFolder+"/canny-phase"+str(it)+".jpg",r)
def processRectangle():
    s, img = cam.read()
    if s: # success
        #red = img.copy()
        #red[:,:,0] = 0
        #red[:,:,1] = 0
        r = cv2.Canny(img,100,200)
        cv2.imwrite(outputFolder+"/rectangle"+str(it)+".jpg",img)
        cv2.imwrite(outputFolder+"/rectangle-phase"+str(it)+".jpg",r)

w.create_rectangle(0,0,sw,sh,outline="#fff",fill="#fff")
for i in range(phases):
    root.after(latency,processRectangle)
    root.after(latency+(delay*i)+1000,iterateLines)
    root.after(latency+((delay+100)*i)+1000,process)

root.mainloop()