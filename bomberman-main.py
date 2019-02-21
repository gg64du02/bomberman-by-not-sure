# import pygame
# import numpy as np
# import keyboard
#
# def main():
#     print("starting")
#     running = True
#     while(running):
#         if(keyboard.is_pressed('esc')):
#             running = False
#             print("stopping issued")
#
# main()

import pygame

import keyboard
import numpy as np

import time
import itertools

def currentMap():
    map = np.ones((15,20))
    for tile in tileGen():
        if(tile[1]%2==1):
            if(tile[0]<10):
                if(tile[0]%2==1):
                    map[tile[1],tile[0]]=0
            else:
                if((tile[0]+1)%2==1):
                    map[tile[1],tile[0]]=0
    return map

def tileGen():
    for line in range(15):
        for row in range(20):
            yield(row,line)

pygame.init()

display_width = 640
display_height = 480

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Bomberman-by-not-sure')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False
# carImg = pygame.image.load('racecar.png')
carImg = pygame.image.load('./sdkskin/Sprites.bmp')
# crateImg = pygame.image.load('./sdkskin/Sprites.bmp')
crateImg = pygame.image.load('./sdkskin/Crate.bmp')
# time.sleep(1)
# crateImg = pygame.image.load(r'C:/Users/jerome/Documents/GitHub/bomberman-by-not-sure/sdkskin/block.bmp')
# crateImg = pygame.image.fromstring(bytes('a'),1,[])
playerRedImg = pygame.image.load('./sdkskin/redPlayer.bmp')

def displayMap():
    for tile in tileGen():
        # print(type(TheMap))
        if(TheMap[tile[1],tile[0]]==0):
            crate(32*tile[0],32*tile[1])


def car(x, y):
    gameDisplay.blit(carImg, (x, y))

def crate(x,y):
    gameDisplay.blit(crateImg, (x, y))

def playerRed(x,y):
    gameDisplay.blit(playerRedImg, (x, y))

def ColisionCheckAndMovement():
    # in : Players, Controls
    # out: Players
    i=0
    # print(Controls.lengh)
    # Controls_from_kbd
    # print("Controls[0]",str(Controls[0]))
    # for player,control in zip(Players,itertools.repeat(Controls_from_kbd)):
    for player,control in zip(Players,Controls_from_kbd):
    # for player,control in zip(Players,Controls):
        print("player,control",player,control)
        # for moveDir,key in zip(player,itertools.repeat(control)):
        #     moveDir += 4 * key


        # player[0] = [Controls]
        playerRed(0,0)
        pass

    pass

def keyboardRead():
    # sfde ctrl shift
    global Controls_from_kbd
    # Controls = [ [0,0,0,0,0,0] for i in range(4)]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                print('KEYDOWN,K_e')
                redPlayerPos[1] -= 1 * 4
                Controls_from_kbd[0][1][3] = 1
            if event.key == pygame.K_s:
                print('KEYDOWN,K_s')
                redPlayerPos[0] -= 1 * 4
                Controls_from_kbd[0][1][0] = 1
            if event.key == pygame.K_f:
                print('KEYDOWN,K_f')
                redPlayerPos[0] += 1 * 4
                Controls_from_kbd[0][1][1] = 1
            if event.key == pygame.K_d:
                print('KEYDOWN,K_d')
                redPlayerPos[1] += 1 * 4
                Controls_from_kbd[0][1][2] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                print('KEYUP,K_e')
                # redPlayerPos[1] -= 1 * 4
                Controls_from_kbd[0][1][3] = 0
            if event.key == pygame.K_s:
                print('KEYUP,K_s')
                # redPlayerPos[0] -= 1 * 4
                Controls_from_kbd[0][1][0] = 0
            if event.key == pygame.K_f:
                print('KEYUP,K_f')
                # redPlayerPos[0] += 1 * 4
                Controls_from_kbd[0][1][1] = 0
            if event.key == pygame.K_d:
                print('KEYUP,K_d')
                # redPlayerPos[1] += 1 * 4
                Controls_from_kbd[0][1][2] = 0


# x = (display_width * 0.45)
# y = (display_height * 0.8)

runningMain = True

redPlayerPos = [0,0]

TheMap = currentMap()
print("TheMap\n",TheMap)
st_time = time.time()

# [[player position_y,player position_x],[bombs available,bombs blast radius]]
Players = [ [[0,0],[1,1]] for i in range(4)]

# global Controls

# sfde ctrl shift
Controls_from_kbd = [ [[0,0,0,0],[0,0]] for j in range(4)]
# Controls_from_kbd = [ [0,0,0,0,0,0] for j in range(4)]
# testControls = np.zeros_like(Controls)
# print("test",test)
# test1 = [[np.zeros(4),np.zeros(2)] for aaa in range (4)]
# Controls = [[np.zeros(4),np.zeros(2)] for aaa in range (4)]
# print("test1",test1)

while(runningMain):
    Controls = keyboardRead()

    ColisionCheckAndMovement()

    # Controls_from_kbd[0][0][0] = 1

    if(keyboard.is_pressed('esc')):
        runningMain = False
        print("issuing the esc key")

    gameDisplay.fill(black)
    # car(x, y)
    # crate(0,0)

    displayMap()
    # playerRed(redPlayerPos[0],redPlayerPos[1])



    pygame.display.update()
    print('time:',str(time.time()-st_time))
    clock.tick(60)
    st_time = time.time()
    # print('lol')

pygame.quit()
quit()