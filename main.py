from tkinter import *
from game import *
from PIL import ImageTk,Image,ImageOps
from enemy import Enemy

def enemy(color, x, y):
    img = Image.open(color + '.jpg')
    img = img.resize((20, 20), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    # enemy_images[color]=img
    i = canvas.create_image(x, y, image=img, tag=color)
    return Enemy(color, i, canvas,img)

ws = Tk()
ws.title('Pacman')
ws.config(bg='#345')

canvas = Canvas(
    ws,
    height=800,
    width=800,
    bg='black'
)

# player
img = Image.open('1200px-Pac_Man.svg.png')
img = img.resize((20, 20), Image.ANTIALIAS)
imgPl = ImageTk.PhotoImage(img)
player1 = canvas.create_image(60, 60, image=imgPl,tag='player')

#ghosts
red=enemy('red',14*40+20, 17*40+20)
green=enemy('green',13*40+20,17*40+20)
yellow=enemy('yellow',15*40+20,15*40+20)
pink=enemy('pink',15*40+20,16*40+20)

# rotation positions
rotations={}

imgLeft=ImageOps.mirror(img)
imgUp=img.rotate(90)
imgDown=img.rotate(-90)

imgRight=ImageTk.PhotoImage(img)
imgLeft = ImageTk.PhotoImage(imgLeft)
imgUp = ImageTk.PhotoImage(imgUp)
imgDown = ImageTk.PhotoImage(imgDown)

rotations = { (-1, 0): imgLeft, (0, -1): imgUp, (0, 1): imgDown, (1, 0): imgRight }

coinMap=[20 * [None] for i in range(20)]

# def ghostReanimation(ghost):


def create_circle(x, y, r, canvasName,i,j,bonus=None): #center coordinates, radius
    if bonus == None:
        color = 'orange'
    else:
        r = 6
        color = 'pink'
    tag=f'{i}x{j}'
    coinMap[i][j]=tag
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,fill=color,tag=tag)
# creating the board
def createBoard(canvas):
    startX=0
    startY=0
    for i in range(20):
        for j in range(20):
            if tiles[i][j]==WALL:
                canvas.create_rectangle(j*40,i*40,
                                        (j+1)*40,(i+1)*40,
                                        fill='blue',outline='blue',tag='wall')
            elif tiles[i][j]==EMPTY:
                create_circle(startX+j*40+20,startY+i*40+20,3,canvas,i,j)
            elif tiles[i][j]==POWER_PELLET_TILE:
                create_circle(startX + j * 40 + 20, startY + i * 40 + 20, 3, canvas, i, j,True)

createBoard(canvas)

imgH = Image.open('heart.png')
imgH = imgH.resize((30, 30), Image.ANTIALIAS)
imgH = ImageTk.PhotoImage(imgH)
canvas.create_image(700, 370, image=imgH, tag='heart')

# for movement
game = Game(canvas,player1,[red,yellow,green,pink],rotations)

ws.bind('<KeyPress-Left>',  game.left)
ws.bind('<KeyPress-Right>',  game.right)
ws.bind('<KeyPress-Up>',  game.up)
ws.bind('<KeyPress-Down>',  game.down)
canvas.pack()
ws.mainloop()