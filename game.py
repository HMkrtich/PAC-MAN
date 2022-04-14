from tkinter import *
import time

# the map of the game
tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

all_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
eating=False

PLAYER_TILE = 2
POWER_PELLET_TILE = 4
WALL=0
EMPTY=1

ALIVE=1
DEAD=0

DIE_TIME=10

GHOST_BONUS=10
COIN_BONUS=1
COIN_NUMBER=160

VELOCITY=5

coinMap=[20 * [False] for i in range(20)]

# global coinMap

class Game:
    def __init__(self,canvas,player,ghosts,rotations):
        # position on board
        self.posX=0
        self.posY=0
        # lives of player
        self.lives=3
        # score of player
        self.score=0
        self.extraScore=0
        self.playing=True
        # to take care movement in x direction
        self.vx = 0
        # to take care movement in y direction
        self.vy = 0
        self.diri=(1,0)
        self.canvas = canvas
        self.canvas.create_text(720, 300, text=f'Score {self.score}',
                                fill='yellow',
                                font=('Helvetica 15 bold'),
                                tag='score')
        self.canvas.create_text(720, 370, text=f'{self.lives}',
                                fill='Red',
                                font=('Helvetica 15 bold'),
                                tag='life')

        # characters
        self.player = player
        self.ghosts=ghosts
        # for timers
        self.rotations=rotations
        self.startTime=None

        global the_game
        the_game=self
        self.canvas.pack()
        self.movement()

    def inDir(self):
        x,y=self.canvas.coords(self.player)
        x1,y1=int(x//40),int(y//40)

        return not (x % 40 == 20 and y % 40 == 20 and tiles[y1+self.vy][x1+self.vx] ==WALL)

    def changeDirection(self,x,y):
        # if pacman can change its direction
        if self.isCross(x, y):
            dirs = self.possibleDir(x, y)
            if self.diri in dirs:
                self.move(self.diri[0], self.diri[1])

        # going in opposite direction
        if self.vx == self.diri[0] * (-1) and self.vy == self.diri[1] * (-1):
            self.move(self.diri[0], self.diri[1])
        tiles[self.posY][self.posX] = EMPTY
        self.posX, self.posY = int(x // 40), int(y // 40)

    def eatPowerPellet(self):
        # if the player eats power pellets
        global eating
        if tiles[self.posY][self.posX] == POWER_PELLET_TILE:
            eating = True
            self.setTimer()
            self.startTime = time.time()
        tiles[self.posY][self.posX] = PLAYER_TILE

    def eatPellet(self):
        if coinMap[self.posY][self.posX]==False:
            tag = f'{self.posY}x{self.posX}'
            self.canvas.delete(tag)
            self.score+=COIN_BONUS
            if self.score==COIN_NUMBER:
                self.winning()
                return
            self.canvas.itemconfigure('score',text=f'Score: {self.score+self.extraScore}')

            coinMap[self.posY][self.posX]=True

    def ghostsTeleport(self):
        for ghost in self.ghosts:
            if ghost.alive:
                ghost.die()
                ghost.reanimate(15*40+20,17*40+20)

    def meetGhosts(self,x,y):
        global eating

        for ghost in self.ghosts:
            endtime=time.time()
            if ghost.alive==False and endtime-ghost.startTime>DIE_TIME:
                ghost.reanimate()
            if ghost.alive and self.isNear(x, y, self.canvas.coords(ghost.ghost)):
                # if the player ate a power pellete
                if eating:
                    self.extraScore += GHOST_BONUS
                    self.canvas.itemconfigure('score', text=f'Score: {self.score + self.extraScore}')
                    ghost.die()
                else:
                    if self.lives > 0:
                        self.respawn()
                        self.lives -= 1
                        self.ghostsTeleport()
                    else:
                        self.canvas.create_text(720, 420, text=f'Game Over',
                                                fill='Red',
                                                font=('Helvetica 15 bold'),
                                                tag='game_over')
                        self.canvas.delete('player')
                        self.endGame()
                    self.canvas.itemconfigure('life', text=f'{self.lives}')

            # if the ghost is killed or not
            if ghost.alive:
                ghost.moveDir()
                self.canvas.move(ghost.ghost, ghost.vx * VELOCITY, ghost.vy * VELOCITY)

    def movement(self):

        endTime = time.time()
        global eating
        if eating:
            remaining = 5 - (endTime - self.startTime)
            self.setTimer(remaining)

            if remaining <= 0:
                eating = False
        # coordiantes of player
        x,y=self.canvas.coords(self.player)
        self.changeDirection(x,y)
        self.eatPowerPellet()
        self.eatPellet()
        if self.playing:
            self.meetGhosts(x,y)
        if self.playing:
            # move player
            self.canvas.move(self.player, VELOCITY*self.vx, VELOCITY*self.vy)
            self.canvas.after(40, self.movement)
            # if the player meets a wall
            if self.inDir()==False:
                self.vx,self.vy=0,0

    # is tile intersection of multiple directions
    def isCross(self, x, y):
        x1,y1=int(x//40),int(y//40)
        return (tiles[y1][x1 + 1] or tiles[y1][x1 - 1]) and \
               (tiles[y1 + 1][x1] or tiles[y1 - 1][x1]) and\
               x%40==y%40==20

    # where can player go
    def possibleDir(self, x, y):
        x1, y1 = int(x // 40), int(y // 40)
        return [(dx, dy) for dx, dy in all_dirs if tiles[y1 + dy][x1 + dx] > WALL]

    def isNear(self, x, y, tup):

        return abs(x - tup[0]) <= 5 and abs(y - tup[1]) <= 5

    def winning(self):
        self.canvas.create_text(720, 450, text=f'Congrats! You Won!',
                                fill='Green',
                                font=('Helvetica 15 bold'),
                                tag='winning')
        self.stopAll()

    def stopAll(self):
        self.vx=0
        self.vy=0
        self.playing=False
        for ghost in self.ghosts:
            ghost.die()

    # respawning of player
    def respawn(self):
        self.canvas.delete('player')
        # player
        direction=self.rotations[self.diri]
        self.player = self.canvas.create_image(180, 140, image=direction, tag='player')

    def endGame(self):
        self.playing=False

    # showing timer while eating ghosts
    def setTimer(self,seconds=5):

        self.canvas.delete('timer')
        if seconds>0:
            seconds = f'{seconds:.2f}'
            self.canvas.create_text(370, 20, text=f'Youve got {seconds} to eat ghosts! Hurry Up!',
                                    fill='Green',
                                    font=('Helvetica 15 bold'),
                                    tag='timer')
        else:
            self.canvas.delete('timer')

    # rotation of player
    def rotation(self,x,y,dir):

        self.canvas.itemconfigure('player', image=self.rotations[dir])

    def left(self,event):
        self.move(-1,0)

    def right(self,event):
        self.move(1,0)

    def up(self,event):
        self.move(0,-1)

    def down(self,event):
        self.move(0,1)

    def move(self, dx, dy):
        if self.playing:
            x, y = self.canvas.coords(self.player)
            x1, y1 = int(x // 40), int(y // 40)
            self.diri = (dx, dy)
            if tiles[y1 + dy][x1 + dx] == EMPTY and \
                    ((self.vx==-dx and self.vy==-dy)or y % 40 == 20 and x % 40 == 20):
                self.vx = dx
                self.vy = dy
                self.rotation(x, y, (dx, dy))



