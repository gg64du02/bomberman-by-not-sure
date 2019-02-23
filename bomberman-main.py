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
    global Players
    # i=0
    for player,control,i in zip(Players,Controls_from_kbd,range(4)):
        print("player,control",player,control)
        # print("i:",i)
        # sfde ctrl shift
        step = 8

        # ==============================================================
        yTmp = player[0][1]
        xTmp = player[0][0]
        # s
        if(control[0][0]==1):
            if(TheMap[int(yTmp/32),int(xTmp/32)]==1):
                xTmp-= step
            # xTmp -= step
            if(xTmp<0):
                xTmp =0
            # if(TheMap[int(yTmp/32),int(xTmp/32)]==0):
            if((TheMap[int(yTmp/32),int(xTmp/32)]==0)or(TheMap[int((yTmp+24)/32),int(xTmp/32)]==0)):
                if((TheMap[int(yTmp/32),int(xTmp/32)]==1)):
                    if(yTmp%32<=16):
                        if(yTmp%32!=0):
                            yTmp-= step
                if((TheMap[int((yTmp+24)/32),int(xTmp/32)]==1)):
                    if(yTmp%32>=16):
                        if(yTmp%32!=0):
                            yTmp+= step
                xTmp+= step
        # f
        if(control[0][1]==1):
            if(TheMap[int(yTmp/32),int(xTmp/32)]==1):
                xTmp += step
            if(xTmp+32>640):
                xTmp =640-32
            # if (TheMap[int((yTmp +0)/ 32), int((xTmp +0)/ 32)] == 0):
            if((TheMap[int((yTmp +0)/ 32), int((xTmp +24)/ 32)] == 0)or(TheMap[int((yTmp +24)/ 32), int((xTmp +24)/ 32)] == 0)):
                if((TheMap[int(yTmp/32),int((xTmp+24)/32)]==1)):
                    if(yTmp%32<=16):
                        if(yTmp%32!=0):
                            yTmp-= step
                if((TheMap[int((yTmp+24)/32),int((xTmp+24)/32)]==1)):
                    if(yTmp%32>=16):
                        if(yTmp%32!=0):
                            yTmp+= step
                xTmp -= step
        # d
        if(control[0][2]==1):
            # if(TheMap[int((yTmp +24)/32),int((xTmp +24)/32)]==1):
            if(TheMap[int((yTmp)/32),int((xTmp)/32)]==1):
                yTmp += step
            if(yTmp+32>480):
                yTmp =480-32
            # if(TheMap[int((yTmp +24)/32),int((yTmp +24)/32)]==0):
            if((TheMap[int((yTmp+24)/32),int((xTmp+0)/32)]==0)or(TheMap[int((yTmp+24)/32),int((xTmp+24)/32)]==0)):
                yTmp-= step
            # if(TheMap[int((yTmp+24)/32),int((xTmp+24)/32)]==0):
            #     yTmp-= step
        # e
        if(control[0][3]==1):
            if (TheMap[int(yTmp / 32), int(xTmp / 32)] == 1):
                yTmp -= step
            if(yTmp<0):
                yTmp =0
            if((TheMap[int((yTmp+0)/32),int((xTmp)/32)]==0)or(TheMap[int((yTmp+0)/32),int((xTmp+24)/32)]==0)):
                yTmp+= step
        player[0][1] = yTmp
        player[0][0] = xTmp


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
                Controls_from_kbd[1][0][3] = 1
            if event.key == pygame.K_s:
                print('KEYDOWN,K_s')
                redPlayerPos[0] -= 1 * 4
                Controls_from_kbd[1][0][0] = 1
            if event.key == pygame.K_f:
                print('KEYDOWN,K_f')
                redPlayerPos[0] += 1 * 4
                Controls_from_kbd[1][0][1] = 1
            if event.key == pygame.K_d:
                print('KEYDOWN,K_d')
                redPlayerPos[1] += 1 * 4
                Controls_from_kbd[1][0][2] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                print('KEYUP,K_e')
                # redPlayerPos[1] -= 1 * 4
                Controls_from_kbd[1][0][3] = 0
            if event.key == pygame.K_s:
                print('KEYUP,K_s')
                # redPlayerPos[0] -= 1 * 4
                Controls_from_kbd[1][0][0] = 0
            if event.key == pygame.K_f:
                print('KEYUP,K_f')
                # redPlayerPos[0] += 1 * 4
                Controls_from_kbd[1][0][1] = 0
            if event.key == pygame.K_d:
                print('KEYUP,K_d')
                # redPlayerPos[1] += 1 * 4
                Controls_from_kbd[1][0][2] = 0


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

while(runningMain):
    Controls = keyboardRead()

    ColisionCheckAndMovement()

    if(keyboard.is_pressed('esc')):
        runningMain = False
        print("issuing the esc key")

    gameDisplay.fill(black)
    # car(x, y)
    # crate(0,0)

    displayMap()

    print("Players[1]",Players[1])
    playerRed(Players[1][0],Players[1][1])



    pygame.display.update()
    print('time:',str(time.time()-st_time))
    clock.tick(20)
    st_time = time.time()
    # print('lol')

pygame.quit()
quit()