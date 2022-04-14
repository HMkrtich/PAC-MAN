import random
import math
import game
import time

class Enemy:
    def __init__(self,name,ghost,canvas,img):
        self.name=name
        self.canvas=canvas
        self.ghost=ghost
        self.vx=0
        self.vy=0
        self.initDir()
        self.img=img
        self.alive=True

    # initializing the first directions of ghosts
    def initDir(self):
        start_dirs = {'red': (1, 0), 'pink': (0, -1), 'green': (-1, 0), 'yellow': (0, 1)}
        self.vx, self.vy = start_dirs[self.name]

    def moveDir(self):
        x,y=self.canvas.coords(self.ghost)
        x1, y1 = int(x // 40), int((y// 40))
        if x%40==20 and y%40==20:
            if self.isCross(x1,y1):

                self.vx, self.vy = self.intersection(x1,y1)

    # is tile intersection of multiple directions
    def isCross(self,x,y):
        return (game.tiles[y][x+1] or game.tiles[y][x-1]) and (game.tiles[y+1][x] or game.tiles[y-1][x])

    # where can ghost go
    def possibleDir(self, x, y):
        return [(dx, dy) for dx, dy in game.all_dirs if game.tiles[y + dy][x + dx] > game.WALL]

    # giving speed
    def giveSpeed(self):
        dx, dy = self.diri
        self.vx = dx
        self.vy = dy

    def intersection(self,x1,y1):
        l1 = self.possibleDir(x1, y1)
        l2 = self.playerQuadrant(x1, y1)

        # 50% of the times the ghost will go random
        if (l2 in l1) and random.randrange(2):
            return l2
        return random.choice(l1)

    # finding where is the player
    def playerQuadrant(self,x,y):
        playerX, playerY = game.the_game.posX, game.the_game.posY
        if abs(x - playerX) > abs(y - playerY):
            dx, dy = math.copysign(1, playerX - x), 0
        else:
            dx, dy = 0, math.copysign(1, playerY - y)

        return (-dx, -dy) if game.eating else (dx, dy)

    # killing ghost
    def die(self):
        self.canvas.delete(self.name)
        self.startTime=time.time()
        self.alive=False

    def reanimate(self,x=300,y=300):
        self.alive = True
        self.ghost = self.canvas.create_image(x, y, image=self.img, tag=self.name)


