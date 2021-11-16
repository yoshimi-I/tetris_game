import tkinter as tk
import random as rd

size = 30
pos_y = 3
pos_x = 5
a = 0
n = rd.randint(0, 3)
tetro1 = [0,0,-1,0,1,0,0,1]
tetro2 = [0,0,-1,0,-1,-1,1,0]
tetro3 = [0,0,-1,0,1,0,2,0]
tetro4 = [0,0,-1,0,0,1,1,1]

ori_tetro1 = [0,0,-1,0,1,0,0,1]
ori_tetro2 = [0,0,-1,0,-1,-1,1,0]
ori_tetro3 = [0,0,-1,0,1,0,2,0]
ori_tetro4 = [0,0,-1,0,0,1,1,1]

rot_list = [0,0]
tetoro_list = [tetro1,tetro2,tetro3,tetro4]
ori_tetro_list = [ori_tetro1,ori_tetro2,ori_tetro3,ori_tetro4]
tetoro_color = ["orange","blue","yellow","green","black","white"]

field = []
for y in range(21):
    field_y = []
    for x in range(12):
        if x == 0 or x == 11 or y == 20:
            field_y.append(5)
        else:
            field_y.append(4)
    field.append(field_y)

def drawField():
    for y in range(21):
        for x in range(12):
            can.create_rectangle(x*size,y*size,(x*size)+size,(y*size)+size,fill = tetoro_color[field[y][x]])

def drawTetoris():
    global tetro1,tetro2,tetro3,tetro4
    tetro1 = ori_tetro1
    tetro2 = ori_tetro2
    tetro3 = ori_tetro3
    tetro4 = ori_tetro4

    for i in range(4):
        x = (tetoro_list[n][i*2]+pos_x)*size
        y = (tetoro_list[n][i*2+1]+pos_y)*size
        can.create_rectangle(x,y,x+size,y+size,fill=tetoro_color[n])

def keyPress(event):
    global pos_x,pos_y
    test_x = pos_x
    test_y = pos_y
    test_list = tetoro_list[n]
    if event.keysym == "Right":
        test_x += 1
    elif event.keysym == "Left":
        test_x -= 1
    elif event.keysym == "Down":
        test_y += 1
    elif event.keysym == "Up":
        test_list = blockRot(tetoro_list[n])
    if checkTest(test_x,test_y):
        pos_x = test_x
        pos_y  = test_y
    if checkRot(test_list):
        tetoro_list[n] = test_list

def blockRot(blockList):
    global rot_list
    rot_list = [0,0]
    for i in range(3):
        y = (blockList[2+(2*i)])
        x = -(blockList[2+(2*i+1)])
        rot_list.append(x)
        rot_list.append(y)
    return rot_list

def checkTest(test_x,test_y):
    result = True
    for i in range(4):
        x = tetoro_list[n][i*2]+test_x
        y = tetoro_list[n][i*2+1]+test_y
        if field[y][x] != 4:
            result = False
    return result

def checkRot(test_list):
    result = True
    for i in range(4):
        x = test_list[i*2]+pos_x
        y = test_list[i*2+1]+pos_y
        if field[y][x] != 4:
            result = False
    return result

def resetBlock(ori_tetro_list,tetoro_list):
    for i in range(4):
        tetoro_list[i] = ori_tetro_list[i]

def nextBlock(test_list):
    global pos_x,pos_y,n
    for i in range(4):
        x = test_list[i*2]+pos_x
        y = test_list[i*2+1]+pos_y
        if field[y+1][x] != 4:
            for j in range(4):
                x = test_list[j*2]+pos_x
                y = test_list[j*2+1]+pos_y
                field[y][x] = n
            pos_y = 0
            pos_x = 5
            n = rd.randint(0, 3)
            resetBlock(ori_tetro_list,tetoro_list)
            drawTetoris()

def deleteBlock():
    for i in range(20):
        if field[i].count(4) == 0:
            
            j = i
            while j >= 1:
                field[j] = field[j-1]
                j -=1

def dropBlock():
    global pos_y
    pos_y += 1
    can.after(800,dropBlock)

win = tk.Tk()
can = tk.Canvas(height = 630,width = 360)
can.pack()

win.bind("<Any-KeyPress>",keyPress)

def gameloop():
    can.delete("all")
    drawField()
    drawTetoris()
    deleteBlock()
    nextBlock(tetoro_list[n])
    can.after(5,gameloop)

gameloop()
dropBlock()


win.mainloop()
