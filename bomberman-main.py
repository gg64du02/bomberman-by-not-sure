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
# Sprites.bmp
print('')
crateImg = pygame.image.load('./sdkskin/Sprites.bmp')


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def crate(x,y):
    gameDisplay.blit(crateImg, (x, y))


x = (display_width * 0.45)
y = (display_height * 0.8)

runningMain = True

while(runningMain):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    if(keyboard.is_pressed('esc')):
        runningMain = False
        print("issuing the esc key")

    gameDisplay.fill(white)
    car(x, y)

    pygame.display.update()
    clock.tick(60)
    print('lol')

pygame.quit()
quit()