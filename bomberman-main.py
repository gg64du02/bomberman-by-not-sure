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
pygame.display.set_caption('A bit Racey')

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

def displayMap():
    for tile in tileGen():
        # print(type(TheMap))
        if(TheMap[tile[1],tile[0]]==0):
            crate(32*tile[0],32*tile[1])


def car(x, y):
    gameDisplay.blit(carImg, (x, y))

def crate(x,y):
    gameDisplay.blit(crateImg, (x, y))

x = (display_width * 0.45)
y = (display_height * 0.8)

runningMain = True

TheMap = currentMap()
print("TheMap\n",TheMap)
st_time = time.time()

while(runningMain):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_LEFT:
            #     print('KEYDOWN,K_LEFT')
            # if event.key == pygame.K_RIGHT:
            #     print('KEYDOWN,K_RIGHT')
            if event.key == pygame.K_e:
                print('KEYDOWN,K_e')
            if event.key == pygame.K_s:
                print('KEYDOWN,K_s')
            if event.key == pygame.K_f:
                print('KEYDOWN,K_f')
            if event.key == pygame.K_d:
                print('KEYDOWN,K_d')
        else:
            pass

    if(keyboard.is_pressed('esc')):
        runningMain = False
        print("issuing the esc key")

    gameDisplay.fill(black)
    # car(x, y)
    # crate(0,0)

    displayMap()



    pygame.display.update()
    print('time:',str(st_time-time.time()))
    clock.tick(60)
    st_time = time.time()
    # print('lol')

pygame.quit()
quit()