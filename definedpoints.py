import tkinter as tk
import math
root = tk.Tk()
root.attributes('-fullscreen',True)

w = tk.Canvas(root,bg='black', highlightthickness=0)

r = []
editingRectangle = False
rc = 0 # rectangle current
pc = 0 # point current

wid = 1800 # editing area width
hei = 1080 # editing area height

colours = [[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255]] # default colours

def renderText(m,l):
    w.create_text(5,10+hei+(l-1)*22,fill="white",font="Times 20 italic bold",text=m,anchor=tk.W)
def createPoint(x,y):
    w.create_oval(x-1,y-1,x+1,y+1,fill="#fff",outline="#fff")

def redraw():
    w.create_rectangle(0,0,wid,hei,fill="black")
    w.create_rectangle(0,hei,wid,hei+100,fill="black")
    renderText("rectangle current: "+str(rc),1)
    renderText("point current: "+str(pc),2)
    if editingRectangle:
        renderText("Editing rectangle",3)
    else:
        renderText("",3)
    it = 0
    for rect in r:
        createPoint(rect[0][0],rect[0][1])
        createPoint(rect[1][0],rect[1][1])
        createPoint(rect[2][0],rect[2][1])
        createPoint(rect[3][0],rect[3][1])
        w.create_polygon([rect[0][0],rect[0][1],rect[1][0],rect[1][1],rect[2][0],rect[2][1],rect[3][0],rect[3][1]],fill=('#%02x%02x%02x'%(colours[it%len(colours)][0],colours[it%len(colours)][1],colours[it%len(colours)][2])))
        it +=1

def createRectangle(e):
    global rc
    global pc
    global editingRectangle
    r.append([[0,0],[0,0],[0,0],[0,0]])
    rc = len(r)-1
    pc = 0
    editingRectangle = True

def movePoint(e):
    if editingRectangle:
        global r
        redraw()
        createPoint(e.x,e.y)

def dist(x1,y1,x2,y2):
    dist = abs(math.sqrt(math.pow(y2-y1,2)+math.pow(x2-x1,2)))
    return dist

def findSnapPoint(x,y):
    for rect in r:
        for pos in rect:
            if dist(x,y,pos[0],pos[1])<20:
                return pos[0],pos[1]
    return x,y

def confirmPoint(e):
    global editingRectangle
    global r
    global pc
    if editingRectangle:
        snapX,snapY = findSnapPoint(e.x,e.y)
        r[rc][pc][0] = snapX
        r[rc][pc][1] = snapY
        pc +=1
        redraw()
        if (pc==4):
            pc = 0
            editingRectangle = False
            w.create_polygon([r[rc][0][0],r[rc][0][1],r[rc][1][0],r[rc][1][1],r[rc][2][0],r[rc][2][1],r[rc][3][0],r[rc][3][1]],fill="#0f0")
            print(r)
            redraw()

redraw()

w.bind('<Button-2>',createRectangle)
w.bind('<Motion>',movePoint)
w.bind('<Button-1>',confirmPoint)
w.pack(fill=tk.BOTH,expand=True)

root.mainloop()