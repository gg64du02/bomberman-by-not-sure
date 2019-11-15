import pygame

import keyboard
import numpy as np

import time
import itertools

import random

# image processing and skin loading
from PIL import Image

# make the display on what's going on the server

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

black = (0, 0, 0)
gray = (127, 127, 127)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False


TheMap = currentMap()
# print("TheMap\n",TheMap)

def displayMap():
    for tile in tileGen():
        # print(type(TheMap))
        if(TheMap[tile[1],tile[0]]==0):
            block(32*tile[0],32*tile[1])

# =============================TILES====================
Tiles = [[[] for lol in range(16)] for lil in range(16)]
# print(Tiles)

image = Image.open("./skin/Tile.png")
# PIL image

for iTiles in range(256):
    x= iTiles%16
    y= int(iTiles/16)

    image2 = image

    width = 32
    height = 32
    box = (32 * x, 32 * y, 32 * x + width, 32 * y + height)
    image3 = image2.crop(box)

    mode = image3.mode
    size = image3.size
    data = image3.tobytes()
    py_image = pygame.image.fromstring(data, size, mode)
    # Surface py_image
    Tiles[y][x] = (py_image)

    # Tiles[y][x]=(pygame.image.load('./sdkskin/spliting/tile_' + str(x) + '_' + str(y) + '.bmp'))

def block(x,y):
    gameDisplay.blit(Tiles[0][0], (x, y))

def crate(x,y):
    gameDisplay.blit(Tiles[4][0], (x, y))

def displayCrates():
    # in: crateMap
    # out: None
    tileGened = tileGen()
    for tile in tileGened:
        xTile = tile[0]
        yTile = tile[1]
        if(crateMap[yTile,xTile]==0):
            crate(32*xTile,32*yTile)

def airBlast(x,y):
    gameDisplay.blit(Tiles[3][0], (x, y))

def displayAirBlasts():
    global airBlasts
    for airBlast in airBlasts:
        # Tiles[3][0-5]
        timePassed = time.time() - airBlast[2]
        print("airBlast",airBlast)
        print("[0+int((2.5*timePassed*1000)/100)]",[0+int((2.5*timePassed*1000)/100)])
        gameDisplay.blit(Tiles[3][0+int((2.5*timePassed*1000)/100)], (32*airBlast[1],32*airBlast[0]))

        if(timePassed*1000>200):
            airBlasts.remove(airBlast)

def diplayAllAirBlast():
    tileGen4  =tileGen()
    for tile in tileGen4:
        if(airBlastDisplay[tile[1],tile[0]]==1):
            airBlast(32*tile[1],32*tile[0])

def displayPlayers():
    for player in Players:
        if (player[2][0] != 0):
            # alive
            gameDisplay.blit(Tiles[ 7+2*player[3][0] ][0], (player[0][0], player[0][1]))
        else:
            # dead
            gameDisplay.blit(Tiles[ 7+2*player[3][0]+1 ][5], (player[0][0], player[0][1]))

def displayBombs():
    # in: listOfBombs
    # out: None
    for bombDis in listOfBombs:
        print("bombDis",bombDis)
        timePassed =  time.time() - bombDis[1]
        print("timePassed",timePassed)
        # max 5+something =11
        gameDisplay.blit(Tiles[1][5+int((3*timePassed*100)/100)], (32*bombDis[0][1],32*bombDis[0][0]))

def displayBrokenCratesAndUpdateCollision(display_on):
    global brokenCrates
    global crateMap
    global lighterMapDisplayList
    for brokenCrate in brokenCrates:
        # Tiles[3][0-7]
        timePassed = time.time() - brokenCrate[2]
        if(display_on==True):
            print("displayBrokenCratesAndUpdateCollision:if(display_on==True):")
            gameDisplay.blit(Tiles[4][0+int((4*timePassed*1000)/100)], (32*brokenCrate[1],32*brokenCrate[0]))
        else:
            print("!displayBrokenCratesAndUpdateCollision:if(display_on==True):")
        if(timePassed*1000>200):
            if(TheMap[brokenCrate[0],brokenCrate[1]]==1):
                crateMap[brokenCrate[0],brokenCrate[1]]=1
            brokenCrates.remove(brokenCrate)
            # lighterMapDisplayList.append([brokenCrate[0],brokenCrate[1]])
            generateItem(brokenCrate[0],brokenCrate[1])


def displayScores():
    for player in Players:
        tmpString = "Player "+str(player[3][0])+" score:"+str(player[4][0])+" | kill(s):"+str(player[4][1])+" | deaths(s):"+str(player[4][2])
        # displayText(tmpString,(display_width / 2), (display_height / 2))
        displayText(tmpString,(display_width / 2), (display_height / 6)+32*player[3][0])
    # displayText("lol",(display_width/2),(display_height/2))
    pass

def displayText(text,x,y):
    # text = "lol"
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    # TextRect.center = ((display_width/2),(display_height/2))
    TextRect.center = (x,y)
    gameDisplay.blit(TextSurf, TextRect)
    # pass

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def displayLighter(x,y):
    gameDisplay.blit(Tiles[6][2], (32*x,32*y))

def displayAdditionnalBomb(x,y):
    gameDisplay.blit(Tiles[6][3], (32*x,32*y))

def displayItems():
    # print("displayLighters")
    # debugging purpose
    # lighterMapDisplayList.append([4,4])
    for lighter in lighterMapDisplayList:
        displayLighter(lighter[1],lighter[0])
    for additionnalBomb in additionnalBombMapDisplayList:
        displayAdditionnalBomb(additionnalBomb[1],additionnalBomb[0])

# doen: add round restart after there one/no players left alive
# todo: remove useless/un-used functions
# done: display scores
# todo:improve score displaying
# todo: fix score counting (when a bomb is exploding underneath)
# done: scores supports
# todo: multiplayers
# done: items spawns and pickup
# done: adding a single file loading all the sprite
# done: adding alpha support for sprites
# done: display all the players
# done: set all the players starting position

# ======================================================

runningMain = True

redPlayerPos = [0,0]

st_time = time.time()

# [[player position_y,player position_x],[bombs available,bombs blast radius]
# ,[alive=1],[i=index for a player],[score,kill,death]]
# Players = [ [[0,0],[1,1],[1],[i]] for i in range(4)]
Players = [ [[0,0],[3,4],[1],[i],[0,0,0]] for i in range(4)]

# Settings starting position
Players[3][0] = [32*0 ,32*14]
Players[2][0] = [32*19,32*0]
Players[1][0] = [32*19,32*14]
Players[0][0] = [32*0 ,32*0]

# global Controls

# sfde ctrl shift
Controls_from_kbd = [ [[0,0,0,0],[0,0]] for j in range(4)]
# Controls_from_kbd = [ [0,0,0,0,0,0] for j in range(4)]

def newRound():
    global runningMain
    global redPlayerPos
    global st_time
    global Players
    global Controls_from_kbd
    # global runningMain
    runningMain = True

    redPlayerPos = [0,0]

    st_time = time.time()

    # [[player position_y,player position_x],[bombs available,bombs blast radius]
    # ,[alive=1],[i=index for a player],[score,kill,death]]
    # Players = [ [[0,0],[1,1],[1],[i]] for i in range(4)]
    Players = [ [[0,0],[3,4],[1],[i],[0,0,0]] for i in range(4)]

    # Settings starting position
    Players[3][0] = [32*0 ,32*14]
    Players[2][0] = [32*19,32*0]
    Players[1][0] = [32*19,32*14]
    Players[0][0] = [32*0 ,32*0]

    # global Controls

    # sfde ctrl shift
    Controls_from_kbd = [ [[0,0,0,0],[0,0]] for j in range(4)]
    # Controls_from_kbd = [ [0,0,0,0,0,0] for j in range(4)]

    global TheMap
    global crateMap
    global lighterMap
    global lighterMapDisplayList
    global additionnalBombMap
    global additionnalBombMapDisplayList
    global lighterMap
    global additionnalBombMap
    TheMap = currentMap()

    crateMap = generatedCrateMap()

    lighterMap = []
    lighterMapDisplayList = []
    additionnalBombMap = []
    additionnalBombMapDisplayList = []
    lighterMap = np.zeros_like(TheMap)
    additionnalBombMap = np.zeros_like(TheMap)

    global airBlastDisplay
    global brokenCrates
    global airBlasts
    global listOfBombs
    airBlastDisplay = np.zeros_like(TheMap)
    brokenCrates = []
    airBlasts = []
    listOfBombs = []
    pass

def numberOfPlayersAlive():
    alivePlayersCount = 0
    for player in Players:
        if (player[2][0]!=0):
            alivePlayersCount +=1
    # print("alivePlayersCount",alivePlayersCount)
    return alivePlayersCount


def generatedCrateMap():
    # in: TheMap
    # out: crateMap
    # done: little better generation
    # todo: add a proper threshold to respect the pourcentageOfCrate
    pourcentageOfCrate = 20
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
            if((100*randomNumber/255)<(pourcentageOfCrate)):
                if(crateMap[yTile,xTile]==1):
                    crateMap[yTile, xTile] = 0
    # print("crateMap\n",crateMap)
    # pass
    return crateMap
crateMap = generatedCrateMap()


lighterMap = []
lighterMapDisplayList =[]
additionnalBombMap=[]
additionnalBombMapDisplayList=[]
lighterMap = np.zeros_like(TheMap)
additionnalBombMap = np.zeros_like(TheMap)

def generateItem(y,x):
    print("generateItem")
    global lighterMap
    global lighterMapDisplayList
    global additionnalBombMap
    global additionnalBombMapDisplayList
    # print("generateItem:[y,x]",[y,x])
    if(TheMap[y,x]!=0):
        # print("if(TheMap[y,x]!=0):")
        if(crateMap[y,x]==1):
            if(random.randint(0,1)%2==0):
                lighterMap[y,x] = 1
                lighterMapDisplayList.append([y,x])
            else:
                # print("[y,x]",[y,x])
                # print("additionnalBombMap\n",additionnalBombMap)
                additionnalBombMap[y][x] = 1
                additionnalBombMapDisplayList.append([y,x])

def playersPickupsItems():
    # for hitboxes()
    # PlayersWhitboxesAindex
    global Players
    global lighterMap
    global lighterMapDisplayList
    for lighter in lighterMapDisplayList:
        for hitbox in PlayersWhitboxesAindex:
            # print("playersPickupsItems:hitbox,lighter:",hitbox,lighter)
            if(np.array_equal([hitbox[1],hitbox[0]],[lighter[1],lighter[0]])):
                # modifying bla st length counts
                Players[hitbox[2]][1][1] += 1
                # updating the lightMap generated
                lighterMap[lighter[0],lighter[1]] = 0
                # removing the lighter
                lighterMapDisplayList.remove(lighter)

    global additionnalBombMap
    global additionnalBombMapDisplayList
    for additionnalBomb in additionnalBombMapDisplayList:
        for hitbox in PlayersWhitboxesAindex:
            # print("playersPickupsItems:hitbox,lighter:",hitbox,lighter)
            if(np.array_equal([hitbox[1],hitbox[0]],[additionnalBomb[1],additionnalBomb[0]])):
                # modifying bombs count
                Players[hitbox[2]][1][0] += 1
                # updating the lightMap generated
                additionnalBombMap[additionnalBomb[0],additionnalBomb[1]] = 0
                # removing the lighter
                additionnalBombMapDisplayList.remove(additionnalBomb)


def ColisionCheckAndMovement():
    # in : Players, Controls
    # out: Players
    global Players
    # i=0
    # print("ColisionCheckAndMovement:Controls_from_kbd",Controls_from_kbd)
    for player,control,i in zip(Players,Controls_from_kbd,range(4)):
        # print("ColisionCheckAndMovement:player,control,i",player,control,i)
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
                if(player[1][0]>0):
                    tryingToPutBomb(player)

def tryingToPutBomb(player):
    # in: player,
    # in/out: (global) listOfBombs
    # [[y, x], loop_time_11]
    global listOfBombs
    global Players
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
                # pos, timestamp, blast length, owner
                listOfBombs.append([[yPos,xPos],time.time(),player[1][1],player[3][0]])
                Players[player[3][0]][1][0] -=1
        else:
            listOfBombs.append([[yPos,xPos],time.time(),player[1][1],player[3][0]])
            Players[player[3][0]][1][0] -=1

def checkForExplodingBomb():
    # in: (global) listOfBombs
    # in: (global) PlayersWhitboxesAindex
    global PlayersWhitboxesAindex
    global Players
    global airBlasts
    responsibleBomb = []
    PlayersWhitboxesAindex = hitboxes()
    for bombExpOrNot in listOfBombs:
        print("bombExpOrNot",bombExpOrNot)
        if((time.time()-bombExpOrNot[1])*1000>2000):
            # print("(time.time()-bombExpOrNot[1])",(time.time()-bombExpOrNot[1]))
            print("if((time.time()-bombExpOrNot[1])<2000):")
            # bomb exploding
            print("listOfBombs",listOfBombs)
            explodingBomb(bombExpOrNot)
            print("checkForExplodingBomb:bombExpOrNot[2]",bombExpOrNot[2])
            responsibleBomb = bombExpOrNot
            # adding the bomb position to the airBlasts (to fix score count about suicide)
            airBlasts.append([bombExpOrNot[0][0],bombExpOrNot[0][1],time.time()])
    # print("PlayersWhitboxesAindex",PlayersWhitboxesAindex)
    # airblasts kills

    if(Players[0][2] == [0]):
        print()

    if (responsibleBomb != []):
        # done: fix the double score count
        for hitbox in PlayersWhitboxesAindex:
            for airBlast in airBlasts:
                # print("checkForExplodingBomb:[hitbox[1],hitbox[0]],[airBlast[1],airBlast[0]]",[hitbox[1],hitbox[0]],[airBlast[1],airBlast[0]])
                if(np.array_equal([hitbox[1],hitbox[0]],[airBlast[1],airBlast[0]])):
                    # print("checkForExplodingBomb:if(np.array_equal([hitbox[1],hitbox[0]],[airBlast[1],airBlast[0]])):")
                    # scoreUpdate
                    if(responsibleBomb[3]==hitbox[2]):
                        # count once
                        # print("Players[hitbox[2]][2][0]",Players[hitbox[2]][2][0])
                        if(Players[hitbox[2]][2][0]!=0):
                            # suicide:works
                            # score
                            Players[responsibleBomb[3]][4][0]-=1
                            # kill: none (suicide)
                            # death
                            Players[responsibleBomb[3]][4][2]+=1

                            # killing players
                            Players[hitbox[2]][2] = [0]
                    else:
                        # count once
                        # print("Players[hitbox[2]][2][0]",Players[hitbox[2]][2][0])
                        if(Players[hitbox[2]][2][0]!=0):
                            # killing another player:works
                            # score
                            Players[responsibleBomb[3]][4][0]+=2
                            # kill: killed another player
                            Players[responsibleBomb[3]][4][1]+=1
                            # death: none (still alive)

                            # adding a death to the killed player
                            Players[hitbox[2]][4][2]+=1

                            # killing players
                            Players[hitbox[2]][2] = [0]


airBlastDisplay = np.zeros_like(TheMap)
brokenCrates = []
airBlasts = []

def explodingBomb(bombExpOrNot):
    # in: bombExpOrNot
    # in: (global) listOfBombs
    # in: (global) Players (killing them) (and checking hitboxes)

    print("explodingBomb:bombExpOrNot",bombExpOrNot)
    Players[bombExpOrNot[3]][1][0] +=1

    # displaying the local blast
    # global airBlastDisplay
    # airBlastDisplay[bombExpOrNot[0][1], bombExpOrNot[0][0]] = 1
    print("explodingBomb:32*bombExpOrNot[0][1],32*bombExpOrNot[0][0]",32*bombExpOrNot[0][1],32*bombExpOrNot[0][0])
    airBlast(32*bombExpOrNot[0][1],32*bombExpOrNot[0][0])

    global listOfBombs

    global brokenCrates

    global airBlasts

    # remaining amount of bombs for the current player
    print("explodingBomb:Players[bombExpOrNot[3]][1][0]", Players[bombExpOrNot[3]][1][0])
    listOfBombs.remove(bombExpOrNot)

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # extend the blast as long as the lengh allow it or if it one crate

    # for bombPosition in listOfBombs:
    # yBomb = bombPosition[0]
    # xBomb = bombPosition[1]
    print("explodingBomb:bombExpOrNot",bombExpOrNot)
    yBomb = bombExpOrNot[0][0]
    xBomb = bombExpOrNot[0][1]
    print("explodingBomb:yBomb,xBomb",yBomb,xBomb)

    pathInBlasts = np.zeros_like(crateMap)


    # done: add blast length support
    # done: stop on crate
    # done: show crate destruction
    # done: air blast display
    # done: killing any players in blasts
    # done: bug hard block destruction display
    # upwward, downward, rightward, leftward
    for i in range(4):
        xTmp = xBomb
        yTmp = yBomb

        # currentBlastLength
        cBL = 0

        tileBombOnce = True
        # DONE bugfix: while ((potentialPath[xTmp, yTmp] == 1) & (isIndexesRange((xTmp, yTmp)))):
        # DONE bugfix: IndexError: index 15 is out of bounds for axis 0 with size 15
        while((crateMap[yTmp, xTmp] == 1) and ( isIndexesRange((yTmp, xTmp)) == True) or (tileBombOnce == True)):
            tileBombOnce = False
            # trigger everything in those blast
            pathInBlasts[yTmp, xTmp] = 1
            if(listOfBombs!=[]):
                for checkingBomb in listOfBombs:
                    print("explodingBomb:[checkingBomb[0][0],checkingBomb[0][1]]",[checkingBomb[0][0],checkingBomb[0][1]])
                    if (np.array_equal([checkingBomb[0][0], checkingBomb[0][1]], [yTmp, xTmp])):
                        print("issuing:explodingBomb(checkingBomb)")
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
            cBL += 1
            # air blast length
            if(cBL>bombExpOrNot[2]):
                break
            # stopping on crate
            if(isIndexesRange((yTmp,xTmp))==True):
                if(crateMap[yTmp,xTmp]==0):
                    # adding the crate to broken one to be later on destroyed upon displaying
                    # and collision removed
                    if(TheMap[yTmp,xTmp]==1):
                        brokenCrates.append([yTmp,xTmp,time.time()])
                        break
                else:
                    # airBlast
                    airBlasts.append([yTmp,xTmp,time.time()])

            print("explodingBomb:[yTmp, xTmp]:",[yTmp, xTmp])

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
    # print("outHitboxes",outHitboxes)
    return outHitboxes

PlayersWhitboxesAindex = hitboxes()

listOfBombs = []

controlsGreenPlayer = [pygame.K_s, pygame.K_f, pygame.K_d, pygame.K_e, pygame.K_z, pygame.K_n]
# controlsGreenPlayer = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP, pygame.K_0, pygame.K_n]
# +0xD0 allow to use the numpad (done: bug fix controlling the red player)
controlsRedPlayer = [pygame.K_4+0xD0, pygame.K_6+0xD0, pygame.K_5+0xD0, pygame.K_8+0xD0, pygame.K_0+0xD0, pygame.K_n]
controlsBluePlayer = [pygame.K_j,pygame.K_l,pygame.K_k,pygame.K_i,pygame.K_SPACE,pygame.K_n]
controlsCyanPlayer = [pygame.K_LEFT,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_UP,pygame.K_RCTRL,pygame.K_n]

controlsForPlayers = [controlsGreenPlayer,controlsRedPlayer,controlsBluePlayer,controlsCyanPlayer]
# controlsForPlayers = [controlsGreenPlayer, controlsRedPlayer]

boolDisplayScores = False

def keyboardRead():
    # sfde ctrl shift
    global Controls_from_kbd

    global boolDisplayScores

    for event in pygame.event.get():
        if(event.type!=4):
            print("event.type",event.type)
        if event.type == pygame.QUIT:
            pass
        if event.type == pygame.KEYDOWN:
            print("pygame.K_TAB",pygame.K_TAB)
            print("event.key",event.key)
            if event.key == pygame.K_TAB:
                boolDisplayScores = True
            for controls,playerNumber in zip(controlsForPlayers,range(0,4)):
                # print("controls",controls)
                for control,index in zip(controls,range(0,5)):
                    # print("control",control)
                    # print("index",index)
                    # 262 is 6 in numpad
                    # print("int(event.key)",int(event.key))
                    if event.key == pygame.K_6:
                        print()
                    if event.key == control :
                        # sfde ctrl shift
                        if(index<4):
                            Controls_from_kbd[playerNumber][0][index]=1
                        else:
                            Controls_from_kbd[playerNumber][1][0]=1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_TAB:
                boolDisplayScores = False
            for controls,playerNumber in zip(controlsForPlayers,range(0,4)):
                # print("controls",controls)
                for control,index in zip(controls,range(0,5)):
                    # print("control",control)
                    # print("index",index)
                    if event.key == control :
                        # sfde ctrl shift
                        if(index<4):
                            Controls_from_kbd[playerNumber][0][index]=0
                        else:
                            Controls_from_kbd[playerNumber][1][0]=0

# if
MASTER_SERVER_DECLARING_PORT = 5007
DEFAULT_HOSTING_A_SERVER_PORT = 5008

from MultiBN import *

# for serialize
import pickle
import sys

def AI_proc(server_ip,number):
    print("AI_proc:"+str(number)+":start")# TCP connexion handling

    # unsure that the server is started
    time.sleep(1)
    import socket

    server_address = (server_ip, DEFAULT_HOSTING_A_SERVER_PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    print("AI_proc:"+str(number)+":socket",s)
    # s.setblocking(0.016)

    st_time  = time.time()

    end_of_round_time = time.time()

    # TODO: multithread on port with port listenning

    # used by the client
    tcpClientGameState = [0 for i in range(0, 7)]
    # 0:conn accepted (by server)
    # 1:number of local players sent (by client)
    # 2:local players accepted (by server)
    incomingDataTCPclient=[]
    arrayIncomingDataTCPclient=[]

    while(True):
        print("AI_proc:==========================================================")
        # socket : start

        # print('AI_proc:waiting for the next event', file=sys.stderr)
        # print(str("AI_proc:"+str(number)+":incomingDataTCPclient "+str(incomingDataTCPclient)), file=sys.stderr)

        outgoingDataTCPclient = []

        if(incomingDataTCPclient!=[]):
            if(incomingDataTCPclient!=b''):
                print("AI_proc:"+str(number)+":incomingDataTCPclient:"+str(incomingDataTCPclient))
                arrayIncomingDataTCPclient = pickle.loads(incomingDataTCPclient)

        print("AI_proc:"+str(number)+":arrayIncomingDataTCPclient",arrayIncomingDataTCPclient)

        if(arrayIncomingDataTCPclient!=[]):
            if(arrayIncomingDataTCPclient[0]=='MBN_SESSION'):
                print("AI_proc:"+str(number)+":if(arrayIncomingDataTCPclient[0]=='MBN_SESSION'):")
                if(arrayIncomingDataTCPclient[1]=='MBN_JOIN_ACCEPTED'):
                    print("AI_proc:" + str(number) + ":if(arrayIncomingDataTCPclient[1]=='MBN_JOIN_ACCEPTED'):")
                    # 0:conn accepted (by server)
                    tcpClientGameState[0]=1
                if(arrayIncomingDataTCPclient[1]=='MBN_JOIN_REFUSED'):
                    print("AI_proc:" + str(number) + ":if(arrayIncomingDataTCPclient[1]=='MBN_JOIN_REFUSED'):")
                    exit()
                if(tcpClientGameState[0]==1):
                    print("AI_proc:"+str(number)+":if(tcpClientGameState[0]==1):")
                    outgoingDataTCPclient = pickle.dumps(['MBN_DATA', "NUMBER_OF_LOCAL_PLAYERS",1])
            if(arrayIncomingDataTCPclient[0]=='MBN_DATA'):
                if(arrayIncomingDataTCPclient[1]=='Players'):
                    print("AI_proc:"+str(number)+":Players:received:",arrayIncomingDataTCPclient[2])
                    outgoingDataTCPclient = pickle.dumps(['MBN_DATA', "Players",Players])

                    # print("AI_proc:" + str(number) + ":current infos:" + str(arrayIncomingDataTCPclient[2][number]))
                    # tmpPlayers = arrayIncomingDataTCPclient[2][number]
                    # print("AI_proc:" + str(number) +"tmpPlayers:"+str(tmpPlayers))
                    # if(abs(tmpPlayers[0][0]-Players[number][0][0])<64):
                    #     if(abs(tmpPlayers[0][1]-Players[number][0][1])<64):
                    #         Players[number] = tmpPlayers



        if (tcpClientGameState[0] == 0):
            outgoingDataTCPclient = pickle.dumps(['MBN_SESSION', 'MBN_JOIN_REQUIRED'])

        if(outgoingDataTCPclient!=[]):
            if(outgoingDataTCPclient!=b''):
                s.send(outgoingDataTCPclient)

        # outgoingDataTCPclient = pickle.dumps(['MBN_DATA', "Players", Players,
        #                                       # "clientSlotKeyboardMapping",clientSlotKeyboardMapping,
        #                                       # "listOfBombsFromClient",listOfBombsFromClient,
        #                                       "Controls_from_kbd", Controls_from_kbd])




        incomingDataTCPclient = s.recv(1024)

        # socket : end

        Controls = keyboardRead()

        ColisionCheckAndMovement()

        if(keyboard.is_pressed('esc')):
            runningMain = False
            print("AI_proc:"+str(number)+":issuing the esc key")

        # gameDisplay.fill(gray)
        # crate(0,0)

        # displayCrates()
        # displayMap()
        # displayBombs()
        print("AI_proc:"+str(number)+":brokenCrates",brokenCrates)
        displayBrokenCratesAndUpdateCollision(False)
        playersPickupsItems()
        # displayAirBlasts()
        # done:Score display is slow
        if(boolDisplayScores == True):
            print("AI_proc:"+str(number)+":displayScores()")
            displayScores()
            # debugging/testing purposes
            # newRound()
        # done: needs to be debugged
        # displayPlayers()
        # displayItems()
        # if more than 1 players are alive, the round can continue
        if(numberOfPlayersAlive()>1):
            end_of_round_time = time.time()
        if((time.time() - end_of_round_time)*1000>3000):
            newRound()
        # for debugging purpose for now
        # diplayAllAirBlast()
        # print("airBlastDisplay\n",airBlastDisplay)

        checkForExplodingBomb()

        # print("hitboxes():\n",hitboxes())

        # pygame.display.update()
        print("AI_proc:"+str(number)+":time:",str((time.time()-st_time)*1000),'ms')
        clock.tick(60)
        st_time = time.time()
        # print('lol')


    print("AI_proc:end")
    pass

def server_proc(ip_on_an_interface,port):
    print("server_proc:start")

    import select
    import socket
    import sys
    import queue

    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    # Bind the socket to the port
    server_address = (ip_on_an_interface, DEFAULT_HOSTING_A_SERVER_PORT)
    # server_address = ('localhost', DEFAULT_HOSTING_A_SERVER_PORT)
    print('server_proc:starting up on {} port {}'.format(*server_address),
          file=sys.stderr)
    server.bind(server_address)
    # Listen for incoming connections
    server.listen(5)
    # Sockets from which we expect to read
    inputs = [server]
    # Sockets to which we expect to write
    outputs = []
    # Outgoing message queues (socket:Queue)
    message_queues = {}

    # number of slots left on server
    slotsLeftOnServer = 4

    st_time  = time.time()

    end_of_round_time = time.time()

    # TODO: multithread on port with port listening

    while(True):
        # print("server_proc:==========================================================")
        # select : start

        # print('server_proc:waiting for the next event', file=sys.stderr)
        # put a ts+0.016<time.time on the select.select() feature maybe ?
        readable, writable, exceptional = select.select(inputs,
                                                        outputs,
                                                        inputs, 0)

        # Handle inputs
        for s in readable:

            if s is server:
                # A "readable" socket is ready to accept a connection
                connection, client_address = s.accept()
                print('server_proc:  connection from', client_address,
                      file=sys.stderr)
                connection.setblocking(0)
                inputs.append(connection)

                # Give the connection a queue for data
                # we want to send
                message_queues[connection] = queue.Queue()

            else:
                data = s.recv(1024)
                if data:
                    incomingDataTCPServer = data
                    print("server_proc:data",data)
                    arrayIncomingDataTCPServer = pickle.loads(data)
                    print("server_proc:arrayIncomingDataTCPServer",arrayIncomingDataTCPServer)
                    if(arrayIncomingDataTCPServer[0]=='MBN_SESSION'):
                        print("server_proc:if(arrayIncomingDataTCPServer[0]=='MBN_SESSION'):")
                        if(arrayIncomingDataTCPServer[1]=='MBN_JOIN_REQUIRED'):
                            if(slotsLeftOnServer==0):
                                # 'MBN_JOIN_REFUSED'
                                print("server_proc:if(slotsLeftOnServer==0):")
                                message_queues[s].put(pickle.dumps(['MBN_SESSION','MBN_JOIN_REFUSED']))
                            else:
                                # 'MBN_JOIN_ACCEPTED'
                                print("server_proc:!if(slotsLeftOnServer==0):")
                                print("server_proc:slotsLeftOnServer:before",slotsLeftOnServer)
                                message_queues[s].put(pickle.dumps(['MBN_SESSION','MBN_JOIN_ACCEPTED']))
                                slotsLeftOnServer -=1
                                print("server_proc:slotsLeftOnServer:after",slotsLeftOnServer)
                                # message_queues[s].put(data)
                        # slotsLeftOnServer
                    else:
                        print("!if(arrayIncomingDataTCPServer[0]=='MBN_SESSION'):")
                    if(arrayIncomingDataTCPServer[0]=='MBN_DATA'):
                        print("server_proc:arrayIncomingDataTCPServer:",arrayIncomingDataTCPServer)
                        if(arrayIncomingDataTCPServer[1]=='NUMBER_OF_LOCAL_PLAYERS'):
                            message_queues[s].put(pickle.dumps(['MBN_DATA',"Players",Players]))
                        if (arrayIncomingDataTCPServer[1] == 'Players'):
                            message_queues[s].put(pickle.dumps(['MBN_DATA',"Players",Players]))

                            pass

                        # outgoingDataTCPclient = pickle.dumps(['MBN_DATA', "NUMBER_OF_LOCAL_PLAYERS", 1])

                    # A readable client socket has data
                    print('server_proc:  received {!r} from {}'.format(
                        data, s.getpeername()), file=sys.stderr,
                    )
                    # message_queues[s].put(data)
                    # Add output channel for response
                    if s not in outputs:
                        outputs.append(s)
                else:
                    # Interpret empty result as closed connection
                    print('server_proc:  closing', client_address,
                          file=sys.stderr)
                    # Stop listening for input on the connection
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

                    # Remove message queue
                    del message_queues[s]
        # Handle outputs
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                # No messages waiting so stop checking
                # for writability.
                print('server_proc:  ', s.getpeername(), 'queue empty',
                      file=sys.stderr)
                outputs.remove(s)
            else:
                print('server_proc:  sending {!r} to {}'.format(next_msg,
                                                    s.getpeername()),
                      file=sys.stderr)
                print("server_proc:pickle.loads(next_msg)",pickle.loads(next_msg))
                s.send(next_msg)
        # Handle "exceptional conditions"
        for s in exceptional:
            print('server_proc:exception condition on', s.getpeername(),
                  file=sys.stderr)
            # Stop listening for input on the connection
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()

            # Remove message queue
            del message_queues[s]
        # time.sleep(1)

        # select : end
        Controls = keyboardRead()

        ColisionCheckAndMovement()

        if(keyboard.is_pressed('esc')):
            runningMain = False
            print("server_proc:issuing the esc key")

        # print("server_proc:brokenCrates",brokenCrates)
        displayBrokenCratesAndUpdateCollision(False)
        playersPickupsItems()
        # displayAirBlasts()
        # done:Score display is slow
        if(boolDisplayScores == True):
            print("server_proc:displayScores()")
            displayScores()
        # if more than 1 players are alive, the round can continue
        if(numberOfPlayersAlive()>1):
            end_of_round_time = time.time()
        if((time.time() - end_of_round_time)*1000>3000):
            newRound()
        # print("airBlastDisplay\n",airBlastDisplay)

        checkForExplodingBomb()

        # print("hitboxes():\n",hitboxes())

        # pygame.display.update()
        # print('server_proc:time:',str((time.time()-st_time)*1000*1000),'us')
        clock.tick(6)
        st_time = time.time()
        # print('lol')

    print("server_proc:end")
    pass

# "architecture"
# # menu() return parameters to start server/AI processes or connect to one
# menu()
# # startProcesses() start a local server and use the infos from menu to start AIs or not
# startProcesses()
# # connect to local server
# display()

def displayTextWsize(text,x,y,fontSize):
    # text = "lol"
    largeText = pygame.font.Font('freesansbold.ttf',fontSize)
    TextSurf, TextRect = text_objects(text, largeText)
    # TextRect.center = ((display_width/2),(display_height/2))
    TextRect.center = (x,y)
    gameDisplay.blit(TextSurf, TextRect)
    # pass

def isMouseInRect(mouse,rect):
    if (mouse[0] > rect[0] and mouse[1] > rect[1]):
        if (mouse[0] < rect[0]+rect[2] and mouse[1] < rect[1]+rect[2]):
            return True
    return False

gameDisplay = []

localHostNumberHumans = 0
localHostNumberAI = 0

def menuDisplay():
    print("menuDisplay:start")
    st_time  = time.time()

    global gameDisplay
    global mainMenuDisplay

    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Bomberman-by-not-sure')

    localHostMenuState = False
    localHostNumberHumansMenuState = False
    chooseTheNumberOfHumansState = False
    chosenTheNumberOfAIState = False
    joinLANorInternetState = False
    lanListingGameState = False
    internetListingGameState = False
    yListDisplayRayOffset = 0

    global localHostNumberHumans
    global localHostNumberAI

    while(True):

        for event in pygame.event.get():
            if(event.type!=4):
                print("event.type", event.type)
            if event.type == pygame.QUIT:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    break
                pass

        gameDisplay.fill(gray)

        white = (255,255,255)
        grey = (200,200,200)
        black = (0,0,0)

        localHostGameButtonColor = grey
        localHostGameButtonRectangle = (50,50,50,50)
        joinGameButtonColor = grey
        joinGameButtonRectangle = (50,150,50,50)
        quitGameButtonColor = grey
        quitGameButtonRectangle = (50,250,50,50)
        if(localHostMenuState == True):
            for i in range(5):
                numberOfHumansGameButtonColor = grey
                numberOfHumansGameButtonRectangle = (100+50,50*i+50,50,50)
                pygame.draw.rect(gameDisplay, numberOfHumansGameButtonColor,numberOfHumansGameButtonRectangle)
                if (isMouseInRect(mouse, numberOfHumansGameButtonRectangle) == True):
                    pygame.draw.rect(gameDisplay, white, (100+50,50*i+50,50,50))
                    if(click[0]==1):
                        localHostNumberHumans = i
                        chooseTheNumberOfHumansState = True
                        chosenTheNumberOfAIState = False
                        pass
        if(chooseTheNumberOfHumansState==True):
            for j in range(5-localHostNumberHumans):
                numberOfAIButtonColor = grey
                numberOfAIButtonRectangle = (100+100+50,50*j+50,50,50)
                pygame.draw.rect(gameDisplay, numberOfAIButtonColor,numberOfAIButtonRectangle)
                if (isMouseInRect(mouse, numberOfAIButtonRectangle) == True):
                    pygame.draw.rect(gameDisplay, white, numberOfAIButtonRectangle)
                    if(click[0]==1):
                        localHostNumberAI = j
                        chosenTheNumberOfAIState = True
                        pass
        if(chosenTheNumberOfAIState==True):
            # print("localHostNumberAI",localHostNumberAI)
            # print("localHostNumberHumans",localHostNumberHumans)
            startGameButtonColor = grey
            startGameButtonRectangle = (300+50,50,50,50)
            pygame.draw.rect(gameDisplay, startGameButtonColor,startGameButtonRectangle)
            if (isMouseInRect(mouse, startGameButtonRectangle) == True):
                pygame.draw.rect(gameDisplay, white, startGameButtonRectangle)
                if(click[0]==1):
                    print("starting the processes")
                    mainMenuDisplay = False
                    break
        if(joinLANorInternetState==True):
            # print("joinLANorInternetState",joinLANorInternetState)
            LanButtonColor = grey
            LanButtonRectangle = (150, 150, 50, 50)
            pygame.draw.rect(gameDisplay, LanButtonColor,LanButtonRectangle)
            if (isMouseInRect(mouse, LanButtonRectangle) == True):
                pygame.draw.rect(gameDisplay, white, LanButtonRectangle)
                if(click[0]==1):
                    lanListingGameState = True
                    internetListingGameState = False
                    # print("joinLANorInternetState")
            InternetButtonColor = grey
            InternetButtonRectangle = (150, 250, 50, 50)
            pygame.draw.rect(gameDisplay, InternetButtonColor,InternetButtonRectangle)
            if (isMouseInRect(mouse, InternetButtonRectangle) == True):
                pygame.draw.rect(gameDisplay, white, InternetButtonRectangle)
                if(click[0]==1):
                    lanListingGameState = False
                    internetListingGameState = True
                    # print("joinLANorInternetState")
        # print("localHostNumberHumans",localHostNumberHumans)
        # print("chosenTheNumberOfAIState",chosenTheNumberOfAIState)
        pygame.draw.rect(gameDisplay, localHostGameButtonColor,localHostGameButtonRectangle)
        pygame.draw.rect(gameDisplay, joinGameButtonColor,joinGameButtonRectangle)
        pygame.draw.rect(gameDisplay, quitGameButtonColor,quitGameButtonRectangle)

        click = pygame.mouse.get_pressed()
        # print(click)
        mouse = pygame.mouse.get_pos()

        if(isMouseInRect(mouse,localHostGameButtonRectangle)==True):
            pygame.draw.rect(gameDisplay, white, localHostGameButtonRectangle)
            if(click[0]==1):
                localHostMenuState = True
                chooseTheNumberOfHumansState = False
                chosenTheNumberOfAIState = False
                joinLANorInternetState = False
                lanListingGameState = False
                pass
        if(isMouseInRect(mouse,joinGameButtonRectangle)==True):
            pygame.draw.rect(gameDisplay, white, joinGameButtonRectangle)
            if(click[0]==1):
                localHostMenuState = False
                chooseTheNumberOfHumansState = False
                chosenTheNumberOfAIState = False
                joinLANorInternetState = True
                pass
        if(isMouseInRect(mouse,quitGameButtonRectangle)==True):
            pygame.draw.rect(gameDisplay, white, quitGameButtonRectangle)
            if(click[0]==1):
                exit()

        displayTextWsize("Local/Host", (50 + 25), (50 + 25), 13)
        displayTextWsize("Join", (50 + 25), (100 + 50 + 25), 13)
        displayTextWsize("Quit/Close", (50 + 25), (200 + 50 + 25), 13)
        if(localHostMenuState == True):
            displayTextWsize("Humans", (50 + 25 + 100), (0 + 25), 13)
            for i in range(5):
                displayTextWsize(str(i), (50 + 25 + 100), (50*i + 50 + 25), 20)
                pygame.draw.line(gameDisplay, black, (100, 50+25), (150, 50+25+50*i), 5)
        if(chooseTheNumberOfHumansState==True):
            displayTextWsize("AI", (100+50 + 25 + 100), (0 + 25), 13)
            for j in range(5-localHostNumberHumans):
                # print("j",j)
                displayTextWsize(str(j), (50 + 25 + 100+100), (50*j + 50 + 25), 20)
                pygame.draw.line(gameDisplay, black, (100+100, 50+25+50*localHostNumberHumans), (100+150, 50+25+50*j), 5)

        # pygame.draw.line(gameDisplay, black, (200, 50+25+50*localHostNumberHumans), (250, 50+25+50*0), 5)
        if(chosenTheNumberOfAIState==True):
            displayTextWsize("Start", (50 + 25 + 300), (50 + 25), 20)
        if(joinLANorInternetState==True):
            displayTextWsize("LAN", 150+25, 150+25, 20)
            displayTextWsize("Internet", 150+25, 250+25, 20)
            pygame.draw.line(gameDisplay, black, (100, 150+25), (150, 250+25), 5)
            pygame.draw.line(gameDisplay, black, (100, 150+25), (150, 150+25), 5)

        lanGames = [(1, "192.168.2.2"), (2, "192.168.2.3"), (3, "192.168.2.4"), (4, "192.168.2.5"), (5, "192.168.2.4"),
                    (6, "192.168.2.6"), (7, "192.168.2.6"), (8, "192.168.2.6"), (9, "192.168.2.6"), (10, "192.168.2.6"),
                    (11, "192.168.2.6")]
        if((lanListingGameState==True) or (internetListingGameState ==True)):
            if(lanListingGameState == True):
                lanGames = lanGames
                yListDisplayRayOffset = 0
            else:
                if(internetListingGameState ==True):
                    # lanGames = internetGames
                    yListDisplayRayOffset = 100
                    # debogging purpose
                    lanGames = lanGames
                else:
                    print("something is wrong in the menu")
            if(len(lanGames)==0):
                pygame.draw.line(gameDisplay, black, (200, 150+25), (250, 150+25), 1)
            for gameIndex in range(len(lanGames)):
                # print("gameIndex",gameIndex)
                xGameDisplay = 250+(gameIndex%4)*100
                yGameDisplay = 50+(gameIndex//4)*100
                pygame.draw.line(gameDisplay, black, (200, 150+25+yListDisplayRayOffset), (xGameDisplay, yGameDisplay+25), 1)
                # pygame.draw.line(gameDisplay, black, (200, 250+25), (xGameDisplay, yGameDisplay+25), 1)
            for gameIndex in range(len(lanGames)):
                xGameDisplay = 250+(gameIndex%4)*100
                yGameDisplay = 50+(gameIndex//4)*100
                gameButtonColor = grey
                gameButtonRectangle = (xGameDisplay,yGameDisplay,50,50)
                pygame.draw.rect(gameDisplay, gameButtonColor,gameButtonRectangle)
                if (isMouseInRect(mouse, gameButtonRectangle) == True):
                    pygame.draw.rect(gameDisplay, white, gameButtonRectangle)
                    if(click[0]==1):
                        mainMenuDisplay = False
                        print("starting the processes")
                displayTextWsize(lanGames[gameIndex][1], xGameDisplay+25, yGameDisplay+25, 10)


        pygame.display.update()
        # print('main:time:', str((time.time() - st_time)*1000*1000),' us')
        clock.tick(6)
        st_time = time.time()
    print("menuDisplay:end")

    pass
# menuDisplay()
# # exit()

import socket

# trying to figure out the IP on the LAN network
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    # doesn't even have to be reachable
    s.connect(('10.255.255.255', 1))
    IP_on_LAN = s.getsockname()[0]
except:
    IP_on_LAN = '127.0.0.1'
finally:
    s.close()
print("IP_on_LAN", IP_on_LAN)

from multiprocessing import Process, freeze_support

if __name__ == '__main__':
    # this is only issued in the main script
    freeze_support()
    # Process(target=server_proc).start()
    mainMenuDisplay = True
    while(True):
        while(mainMenuDisplay==True):
            menuDisplay()
        # todo: merge the server and client (Can be AI or the display) select code to allow for easier dev
        # todo: connect the display to allow the debugging
        # server_ip = '192.168.1.99'
        server_ip = IP_on_LAN
        Process(target=server_proc, args=(server_ip,DEFAULT_HOSTING_A_SERVER_PORT,)).start()
        time.sleep(1)
        for aiIndex in range(localHostNumberAI):
            print("aiIndex",aiIndex)
            Process(target=AI_proc,args=(server_ip,aiIndex,)).start()
        # =========================================================================
        # =========================================================================
        import select
        import socket
        import sys
        import queue

        # Create a TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server.setblocking(0)
        # Bind the socket to the port
        server_address = (server_ip, DEFAULT_HOSTING_A_SERVER_PORT)
        # server_address = ('localhost', DEFAULT_HOSTING_A_SERVER_PORT)
        print('gameDisplay:starting up on {} port {}'.format(*server_address),
              file=sys.stderr)
        server.connect(server_address)
        # server.bind(server_address)
        # Listen for incoming connections
        # server.listen(5)
        # Sockets from which we expect to read
        inputs = [server]
        # Sockets to which we expect to write
        outputs = []
        # Outgoing message queues (socket:Queue)
        message_queues = {}
        # =========================================================================
        # =========================================================================

        st_time  = time.time()

        end_of_round_time = time.time()


        gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('Bomberman-by-not-sure')

        end_of_round_time = time.time()

        print("gameDisplay:1")

        kickstartTheDisplay = False

        while(runningMain):
            print("gameDisplay:==========================================================")
            # =========================================================================
            # =========================================================================
            # readable, writable, exceptional = select.select(inputs,
            #                                                 outputs,
            #                                                 inputs, 0)

            print("gameDisplay:2")

            # print("gameDisplay:readable, writable, exceptional",readable, writable, exceptional)
            print("gameDisplay:server",server)

            server.send(pickle.dumps(['MBN_DATA', "Players", Players]))

            dataGameDisplay = server.recv(1024)
            print("gameDisplay:dataGameDisplay:dataGameDisplay",dataGameDisplay)
            tmpIncomingInfo = pickle.loads(dataGameDisplay)
            print("gameDisplay:tmpIncomingInfo[2]",tmpIncomingInfo[2])
            
            # if(kickstartTheDisplay==True):
            #     # ask the server for an update
            # message_queues[s].put(pickle.dumps(['MBN_DATA', "Players", Players]))

            # # Handle inputs
            # for s in readable:
            #     print("gameDisplay:readable:3")
            #
            #     if s is server:
            #         print("gameDisplay:4")
            #         # A "readable" socket is ready to accept a connection
            #         connection, client_address = s.accept()
            #         print('gameDisplay:  connection from', client_address,
            #               file=sys.stderr)
            #         connection.setblocking(0)
            #         inputs.append(connection)
            #
            #         # Give the connection a queue for data
            #         # we want to send
            #         message_queues[connection] = queue.Queue()
            #
            #     else:
            #         print("gameDisplay:readable:5")
            #         data = s.recv(1024)
            #         print("gameDisplay:readable:6")
            #
            #         if data:
            #             incomingDataTCPServer = data
            #             print("gameDisplay:data",data)
            #             arrayIncomingDataTCPServer = pickle.loads(data)
            #             print("gameDisplay:arrayIncomingDataTCPServer",arrayIncomingDataTCPServer)
            #             if(arrayIncomingDataTCPServer[0]=='MBN_SESSION'):
            #                 print("gameDisplay:if(arrayIncomingDataTCPServer[0]=='MBN_SESSION'):")
            #                 if(arrayIncomingDataTCPServer[1]=='MBN_JOIN_REQUIRED'):
            #                     if(slotsLeftOnServer==0):
            #                         # 'MBN_JOIN_REFUSED'
            #                         print("gameDisplay:if(slotsLeftOnServer==0):")
            #                         message_queues[s].put(pickle.dumps(['MBN_SESSION','MBN_JOIN_REFUSED']))
            #                     else:
            #                         # 'MBN_JOIN_ACCEPTED'
            #                         print("gameDisplay:!if(slotsLeftOnServer==0):")
            #                         print("gameDisplay:slotsLeftOnServer:before",slotsLeftOnServer)
            #                         message_queues[s].put(pickle.dumps(['MBN_SESSION','MBN_JOIN_ACCEPTED']))
            #                         slotsLeftOnServer -=1
            #                         print("gameDisplay:slotsLeftOnServer:after",slotsLeftOnServer)
            #                         # message_queues[s].put(data)
            #                 # slotsLeftOnServer
            #             else:
            #                 print("!if(arrayIncomingDataTCPServer[0]=='MBN_SESSION'):")
            #             if(arrayIncomingDataTCPServer[0]=='MBN_DATA'):
            #                 if(arrayIncomingDataTCPServer[1]=='NUMBER_OF_LOCAL_PLAYERS'):
            #                     # message_queues[s].put(pickle.dumps(['MBN_DATA','clientSlotKeyboardMapping',clientSlotKeyboardMapping]))
            #
            #                 # if(arrayIncomingDataTCPclient[1]=='Players'):
            #                 #     arrayIncomingDataTCPclient[2]
            #                     print("gameDisplay:arrayIncomingDataTCPServer" ,arrayIncomingDataTCPServer)
            #                     kickstartTheDisplay = True
            #
            #                     pass
            #
            #                 # outgoingDataTCPclient = pickle.dumps(['MBN_DATA', "NUMBER_OF_LOCAL_PLAYERS", 1])
            #
            #             # A readable client socket has data
            #             print('gameDisplay:  received {!r} from {}'.format(
            #                 data, s.getpeername()), file=sys.stderr,
            #             )
            #             # message_queues[s].put(data)
            #             # Add output channel for response
            #             if s not in outputs:
            #                 outputs.append(s)
            #         else:
            #             # Interpret empty result as closed connection
            #             print('gameDisplay:  closing', client_address,
            #                   file=sys.stderr)
            #             # Stop listening for input on the connection
            #             if s in outputs:
            #                 outputs.remove(s)
            #             inputs.remove(s)
            #             s.close()
            #
            #             # Remove message queue
            #             del message_queues[s]
            # # Handle outputs
            # for s in writable:
            #
            #     try:
            #         next_msg = message_queues[s].get_nowait()
            #     except queue.Empty:
            #         # No messages waiting so stop checking
            #         # for writability.
            #         print('gameDisplay:  ', s.getpeername(), 'queue empty',
            #               file=sys.stderr)
            #         outputs.remove(s)
            #     else:
            #         print('gameDisplay:  sending {!r} to {}'.format(next_msg,
            #                                             s.getpeername()),
            #               file=sys.stderr)
            #         print("gameDisplay:pickle.loads(next_msg)",pickle.loads(next_msg))
            #         s.send(next_msg)
            # # Handle "exceptional conditions"
            # for s in exceptional:
            #     print('gameDisplay:exception condition on', s.getpeername(),
            #           file=sys.stderr)
            #     # Stop listening for input on the connection
            #     inputs.remove(s)
            #     if s in outputs:
            #         outputs.remove(s)
            #     s.close()
            #
            #     # Remove message queue
            #     del message_queues[s]
            # # time.sleep(1)

            # =========================================================================
            # =========================================================================

            Controls = keyboardRead()

            ColisionCheckAndMovement()

            if(keyboard.is_pressed('esc')):
                runningMain = False
                print("gameDisplay:issuing the esc key")

            gameDisplay.fill(gray)
            # crate(0,0)

            displayCrates()
            displayMap()
            displayBombs()
            # print("main:brokenCrates",brokenCrates)
            displayBrokenCratesAndUpdateCollision(True)
            playersPickupsItems()
            displayAirBlasts()
            # done:Score display is slow
            if(boolDisplayScores == True):
                print("gameDisplay:displayScores()")
                displayScores()
                # debugging/testing purposes
                # newRound()
            # done: needs to be debugged
            displayPlayers()
            displayItems()
            # if more than 1 players are alive, the round can continue
            if(numberOfPlayersAlive()>1):
                end_of_round_time = time.time()
            if((time.time() - end_of_round_time)*1000>3000):
                newRound()
            # for debugging purpose for now
            # diplayAllAirBlast()
            # print("airBlastDisplay\n",airBlastDisplay)

            checkForExplodingBomb()

            # print("hitboxes():\n",hitboxes())

            pygame.display.update()
            # print('main:time:',str(time.time()-st_time))
            clock.tick(3)
            st_time = time.time()
            # print('lol')

        pygame.quit()
        quit()