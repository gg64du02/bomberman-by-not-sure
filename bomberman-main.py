import pygame

import keyboard
import numpy as np

import time
import itertools

import random

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
blockImg = pygame.image.load('./sdkskin/Block.bmp')
crateImg = pygame.image.load('./sdkskin/Crate.bmp')
# time.sleep(1)
# crateImg = pygame.image.load(r'C:/Users/jerome/Documents/GitHub/bomberman-by-not-sure/sdkskin/block.bmp')
# crateImg = pygame.image.fromstring(bytes('a'),1,[])
playerRedImg = pygame.image.load('./sdkskin/redPlayer.bmp')
bombImg = pygame.image.load('./sdkskin/Bomb.bmp')


TheMap = currentMap()
print("TheMap\n",TheMap)

def displayMap():
    for tile in tileGen():
        # print(type(TheMap))
        if(TheMap[tile[1],tile[0]]==0):
            block(32*tile[0],32*tile[1])

# =============================TILES====================
def car(x, y):
    gameDisplay.blit(carImg, (x, y))

def block(x,y):
    gameDisplay.blit(blockImg, (x, y))

def crate(x,y):
    gameDisplay.blit(crateImg, (x, y))

def playerRed(x,y):
    gameDisplay.blit(playerRedImg, (x, y))

def bomb(x,y):
    gameDisplay.blit(bombImg, (x, y))

# ======================================================

runningMain = True

redPlayerPos = [0,0]

st_time = time.time()

# [[player position_y,player position_x],[bombs available,bombs blast radius]
# ,[alive=1],[i=index for a player]]
# Players = [ [[0,0],[1,1],[1],[i]] for i in range(4)]
Players = [ [[0,0],[3,3],[1],[i]] for i in range(4)]

# global Controls

# sfde ctrl shift
Controls_from_kbd = [ [[0,0,0,0],[0,0]] for j in range(4)]
# Controls_from_kbd = [ [0,0,0,0,0,0] for j in range(4)]

def generatedCrateMap():
    # in: TheMap
    # out: crateMap
    # todo: add a proper threshold to respect the pourcentageOfCrate
    pourcentageOfCrate = 80
    minFreeSpot = 12
    tileGened = tileGen()
    crateMap = np.copy(TheMap)
    # freePoints = [[0,0],[0,1],[1,0], [19,14],[18,14],[19,13]]
    freePoints = [[0,0],[0,1],[1,0], [19,14],[18,14],[19,13], [19,0],[18,0],[19,1], [0,14],[1,13],[1,14]]
    for tile in tileGened:
        # print("tile",tile)
        xTile = tile[0]
        yTile = tile[1]
        # randNp = np.random.rand(20,15)
        # print("randNp:\n",randNp)
        randomNumber = random.randint(0,255)
        # print("randomNumber",randomNumber)
        if(not([xTile,yTile] in freePoints)):
            # print([xTile,yTile])
            if((100*randomNumber/255)>(pourcentageOfCrate)):
                if(crateMap[yTile,xTile]==1):
                    crateMap[yTile, xTile] = 0
    print("crateMap\n",crateMap)
    # pass
    return crateMap
crateMap = generatedCrateMap()

def displayCrates():
    # in: crateMap
    # out: None
    tileGened = tileGen()
    for tile in tileGened:
        xTile = tile[0]
        yTile = tile[1]
        if(crateMap[yTile,xTile]==0):
            crate(32*xTile,32*yTile)


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
        if(player[2][0]==1):
        # if(player[2]==1):
            # s
            if(control[0][0]==1):
                if(crateMap[int(yTmp/32),int(xTmp/32)]==1):
                    xTmp-= step
                # xTmp -= step
                if(xTmp<0):
                    xTmp =0
                # if(crateMap[int(yTmp/32),int(xTmp/32)]==0):
                if((crateMap[int(yTmp/32),int(xTmp/32)]==0)or(crateMap[int((yTmp+24)/32),int(xTmp/32)]==0)):
                    if((crateMap[int(yTmp/32),int(xTmp/32)]==1)):
                        if(yTmp%32<=16):
                            if(yTmp%32!=0):
                                yTmp-= step
                    if((crateMap[int((yTmp+24)/32),int(xTmp/32)]==1)):
                        if(yTmp%32>=16):
                            if(yTmp%32!=0):
                                yTmp+= step
                    xTmp+= step
            # f
            if(control[0][1]==1):
                if(crateMap[int(yTmp/32),int(xTmp/32)]==1):
                    xTmp += step
                if(xTmp+32>640):
                    xTmp =640-32
                # if (crateMap[int((yTmp +0)/ 32), int((xTmp +0)/ 32)] == 0):
                if((crateMap[int((yTmp +0)/ 32), int((xTmp +24)/ 32)] == 0)or(crateMap[int((yTmp +24)/ 32), int((xTmp +24)/ 32)] == 0)):
                    if((crateMap[int(yTmp/32),int((xTmp+24)/32)]==1)):
                        if(yTmp%32<=16):
                            if(yTmp%32!=0):
                                yTmp-= step
                    if((crateMap[int((yTmp+24)/32),int((xTmp+24)/32)]==1)):
                        if(yTmp%32>=16):
                            if(yTmp%32!=0):
                                yTmp+= step
                    xTmp -= step
            # d
            if(control[0][2]==1):
                # if(crateMap[int((yTmp +24)/32),int((xTmp +24)/32)]==1):
                if(crateMap[int((yTmp)/32),int((xTmp)/32)]==1):
                    yTmp += step
                if(yTmp+32>480):
                    yTmp =480-32
                # if(crateMap[int((yTmp +24)/32),int((yTmp +24)/32)]==0):
                if((crateMap[int((yTmp+24)/32),int((xTmp+0)/32)]==0)or(crateMap[int((yTmp+24)/32),int((xTmp+24)/32)]==0)):
                    if((crateMap[int((yTmp+24)/32),int((xTmp+0)/32)]==1)):
                        if(xTmp%32<=16):
                            if(xTmp%32!=0):
                                xTmp-= step
                    if((crateMap[int((yTmp+24)/32),int((xTmp+24)/32)]==1)):
                        if(xTmp%32>=16):
                            if(xTmp%32!=0):
                                xTmp+= step
                    yTmp-= step
                # if(crateMap[int((yTmp+24)/32),int((xTmp+24)/32)]==0):
                #     yTmp-= step
            # e
            if(control[0][3]==1):
                if (crateMap[int(yTmp / 32), int(xTmp / 32)] == 1):
                    yTmp -= step
                if(yTmp<0):
                    yTmp =0
                if((crateMap[int((yTmp+0)/32),int((xTmp)/32)]==0)or(crateMap[int((yTmp+0)/32),int((xTmp+24)/32)]==0)):
                    if ((crateMap[int((yTmp + 0) / 32), int((xTmp + 0) / 32)] == 1)):
                        if (xTmp % 32 <= 16):
                            if (xTmp % 32 != 0):
                                xTmp -= step
                    if ((crateMap[int((yTmp + 0) / 32), int((xTmp + 24) / 32)] == 1)):
                        if (xTmp % 32 >= 16):
                            if (xTmp % 32 != 0):
                                xTmp += step
                    yTmp+= step
            player[0][1] = yTmp
            player[0][0] = xTmp

            # ctrl
            if(control[1][0]==1):
                print("if(control[1][1]==1):")
                tryingToPutBomb(player)

def tryingToPutBomb(player):
    # in: player,
    # in/out: (global) listOfBombs
    # [[y, x], loop_time_11]
    global listOfBombs
    # xPos = player[0][0]
    # yPos = player[0][1]
    xPos = int((player[0][0] +16)/32)
    yPos = int((player[0][1] +16)/32)
    print("tryingToPutBomb:xPos,yPos",xPos,yPos)
    # does the player still have remaining bombs to put
    if(player[1][0] != 0):
        if(listOfBombs!=[]):
            # print("listOfBombs[:,0]",listOfBombs[:,0])
            alreadyBusy = False
            for tmpBomb in listOfBombs:
                print([yPos,xPos],tmpBomb[0])
                if(np.array_equal([yPos,xPos],tmpBomb[0])==1):
                    alreadyBusy = True
            # if the place is empty
            if(alreadyBusy==False):
                # pos, timestamp, blast lenght, owner
                listOfBombs.append([[yPos,xPos],time.time(),player[1][1],player[3][0]])
        else:
            listOfBombs.append([[yPos,xPos],time.time(),player[1][1],player[3][0]])
            player[1][0] -=1

def displayBombs():
    # in: listOfBombs
    # out: None
    for bombDis in listOfBombs:
        # print("bombDis",bombDis)
        # print(bombDis[0][1],bombDis[0][0])
        bomb(32*bombDis[0][1],32*bombDis[0][0])

def checkForExplodingBomb():
    # in: (global) listOfBombs
    # in: (global) PlayersWhitboxesAindex
    global PlayersWhitboxesAindex
    global Players
    for bombExpOrNot in listOfBombs:
        print("bombExpOrNot",bombExpOrNot)
        if((time.time()-bombExpOrNot[1])*1000>2000):
            PlayersWhitboxesAindex = hitboxes()
            # print("(time.time()-bombExpOrNot[1])",(time.time()-bombExpOrNot[1]))
            print("if((time.time()-bombExpOrNot[1])<2000):")
            # bomb exploding
            explodingBomb(bombExpOrNot)
            print("checkForExplodingBomb:bombExpOrNot[2]",bombExpOrNot[2])
            Players[bombExpOrNot[3]][1][0] +=1
    pass

def explodingBomb(bombExpOrNot):
    # in: bombExpOrNot
    # in: (global) listOfBombs
    # in: (global) Players (killing them) (and checking hitboxes)

    # kill anything under the bomb
    for hitbox in PlayersWhitboxesAindex:
        if(np.array_equal([hitbox[0],hitbox[1]],[bombExpOrNot[0][0],bombExpOrNot[0][1]])==1):
            Players[hitbox[2]][2] = [0]
            print("hitbox[2]",hitbox[2])
            print("player",Players[hitbox[2]],"got killed")

    print("Players[bombExpOrNot[2]][1][0]", Players[bombExpOrNot[2]][1][0])
    listOfBombs.remove(bombExpOrNot)

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # extend the blast as long as the lengh allow it or if it one crate

    # pathInBlasts = np.zeros_like(potentialPath)
    # for bombPosition in listOfBombs:
    # yBomb = bombPosition[0]
    # xBomb = bombPosition[1]
    print("bombExpOrNot",bombExpOrNot)
    yBomb = bombExpOrNot[0][0]
    xBomb = bombExpOrNot[0][1]

    pathInBlasts = np.zeros_like(crateMap)

    # notsorted
    # TODO: sort the result
    # upwward, downward, rightward, leftward
    for i in range(4):
        xTmp = xBomb
        yTmp = yBomb

        tileBombOnce = True
        # DONE bugfix: while ((potentialPath[xTmp, yTmp] == 1) & (isIndexesRange((xTmp, yTmp)))):
        # DONE bugfix: IndexError: index 15 is out of bounds for axis 0 with size 15
        while((crateMap[yTmp, xTmp] == 1) and ( isIndexesRange((yTmp, xTmp)) == True) or (tileBombOnce == True)):
            tileBombOnce = False
            # trigger everything in those blast
            pathInBlasts[yTmp, xTmp] = 1
            if(listOfBombs!=[]):
                for checkingBomb in listOfBombs:
                    if(np.array_equal([checkingBomb[0][1],checkingBomb[0][0]],[yTmp,xTmp])):
                        explodingBomb(checkingBomb)
            if (i == 0):
                xTmp += 1
                if (isIndexesRange((0, xTmp)) == False):
                    break
            if (i == 1):
                xTmp -= 1
                if (isIndexesRange((0, xTmp)) == False):
                    break
            if (i == 2):
                yTmp += 1
                if (isIndexesRange((yTmp, 0)) == False):
                    break
            if (i == 3):
                yTmp -= 1
                if (isIndexesRange((yTmp, 0)) == False):
                    break
            # print("[yTmp, xTmp]:",[yTmp, xTmp])

    print("pathInBlasts\n",pathInBlasts)


    # for bombExpOrNotExp in listOfBombs:
    #     explodingBomb(bombExpOrNotExp)
    pass

def isIndexesRange(point):
    isInsideIndexRange = False
    if (point[1] >= 0):
        if (point[1] < 20):
            if (point[0] >= 0):
                if (point[0] < 15):
                    # print("ii in (0,0) and (19,15)")
                    isInsideIndexRange = True
    return isInsideIndexRange

def hitboxes():
    # in: Players
    # out: PlayersWhitboxesAindex
    outHitboxes =[]
    for player in Players:
        outHitboxes.append([int((player[0][1]+2)/32),int((player[0][0]+2)/32),player[3][0]])
        outHitboxes.append([int((player[0][1]+30)/32),int((player[0][0]+30)/32),player[3][0]])
        # pass
    print("outHitboxes",outHitboxes)
    return outHitboxes

PlayersWhitboxesAindex = hitboxes()

listOfBombs = []


def keyboardRead():
    # sfde ctrl shift
    global Controls_from_kbd
    # Controls = [ [0,0,0,0,0,0] for i in range(4)]
    for event in pygame.event.get():
        print("event.type",event.type)
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
            if event.key == pygame.K_z:
                Controls_from_kbd[1][1][0] = 1
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
            if event.key == pygame.K_z:
                Controls_from_kbd[1][1][0] = 0



while(runningMain):
    Controls = keyboardRead()

    ColisionCheckAndMovement()

    if(keyboard.is_pressed('esc')):
        runningMain = False
        print("issuing the esc key")

    gameDisplay.fill(black)
    # car(x, y)
    # crate(0,0)

    displayCrates()
    displayMap()
    displayBombs()
    checkForExplodingBomb()

    print("hitboxes():\n",hitboxes())

    print("Players[1]",Players[1])
    playerRed(Players[1][0],Players[1][1])



    pygame.display.update()
    print('time:',str(time.time()-st_time))
    clock.tick(40)
    st_time = time.time()
    # print('lol')

pygame.quit()
quit()