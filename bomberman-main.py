import pygame

import keyboard
import numpy as np

import time
import itertools

import random

# image processing and skin loading
from PIL import Image

# for serialize
import pickle

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
gray = (127, 127, 127)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False


TheMap = currentMap()
print("TheMap\n",TheMap)

def displayMap():
    for tile in tileGen():
        # print(type(TheMap))
        if(TheMap[tile[1],tile[0]]==0):
            block(32*tile[0],32*tile[1])

# =============================TILES====================
Tiles = [[[] for lol in range(16)] for lil in range(16)]
print(Tiles)

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
        # print("airBlast",airBlast)
        # print("[0+int((2.5*timePassed*1000)/100)]",[0+int((2.5*timePassed*1000)/100)])
        if(isIndexesRangeTileRange([3,0+int((2.5*timePassed*1000)/100)])==True):
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
        # print("bombDis",bombDis)
        timePassed =  time.time() - bombDis[1]
        # print("timePassed",timePassed)
        # max 5+something =11
        gameDisplay.blit(Tiles[1][5+int((3*timePassed*100)/100)], (32*bombDis[0][1],32*bombDis[0][0]))

def displayBrokenCratesAndUpdateCollision():
    global brokenCrates
    global crateMap
    global lighterMapDisplayList
    for brokenCrate in brokenCrates:
        # Tiles[3][0-7]
        timePassed = time.time() - brokenCrate[2]
        if(isIndexesRangeTileRange([4,0+int((4*timePassed*1000)/100)])==True):
            print("brokenCrates",brokenCrates)
            print("[4,0+int((4*timePassed*1000)/100)]",[4,0+int((4*timePassed*1000)/100)])
            gameDisplay.blit(Tiles[4][0+int((4*timePassed*1000)/100)], (32*brokenCrate[1],32*brokenCrate[0]))
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
    print("crateMap\n",crateMap)
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
                if(not [y,x] in lighterMapDisplayList):
                    lighterMap[y,x] = 1
                    lighterMapDisplayList.append([y,x])
            else:
                # print("[y,x]",[y,x])
                # print("additionnalBombMap\n",additionnalBombMap)
                if(not [y,x] in additionnalBombMapDisplayList):
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
                print("lighterMapDisplayList",lighterMapDisplayList)
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
                print("additionnalBombMapDisplayList",additionnalBombMapDisplayList)
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
        if(clientSlotKeyboardMapping != []):
            if(clientSlotKeyboardMapping[i]==0):
                # print("ColisionCheckAndMovement:continue")
                continue
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
                # print("if(control[1][1]==1):")
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
    # print("tryingToPutBomb:xPos,yPos",xPos,yPos)
    # does the player still have remaining bombs to put
    if(player[1][0] != 0):
        # if(listOfBombs!=[]):
        if(Players[player[3][0]][1][0]>0):
            # print("listOfBombs[:,0]",listOfBombs[:,0])
            alreadyBusy = False
            for tmpBomb in listOfBombs:
                # print([yPos,xPos],tmpBomb[0])
                if(np.array_equal([yPos,xPos],tmpBomb[0])==1):
                    alreadyBusy = True
            # if the place is empty
            if(alreadyBusy==False):
                # pos, timestamp, blast length, owner
                listOfBombs.append([[yPos,xPos],time.time(),player[1][1],player[3][0]])
                Players[player[3][0]][1][0] -=1
        # else:
        #     listOfBombs.append([[yPos,xPos],time.time(),player[1][1],player[3][0]])
        #     Players[player[3][0]][1][0] -=1

def checkForExplodingBomb():
    # in: (global) listOfBombs
    # in: (global) PlayersWhitboxesAindex
    global PlayersWhitboxesAindex
    global Players
    global airBlasts
    responsibleBomb = []
    PlayersWhitboxesAindex = hitboxes()
    for bombExpOrNot in listOfBombs:
        # print("checkForExplodingBomb:bombExpOrNot",bombExpOrNot)
        if((time.time()-bombExpOrNot[1])*1000>2000):
            # print("(time.time()-bombExpOrNot[1])",(time.time()-bombExpOrNot[1]))
            # print("if((time.time()-bombExpOrNot[1])<2000):")
            # bomb exploding
            # print("listOfBombs",listOfBombs)
            explodingBomb(bombExpOrNot)
            # print("checkForExplodingBomb:bombExpOrNot[2]",bombExpOrNot[2])
            responsibleBomb = bombExpOrNot
            # adding the bomb position to the airBlasts (to fix score count about suicide)
            airBlasts.append([bombExpOrNot[0][0],bombExpOrNot[0][1],time.time()])
    # print("PlayersWhitboxesAindex",PlayersWhitboxesAindex)
    # airblasts kills

    # if(Players[0][2] == [0]):
    #     print()

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

    # print("explodingBomb:bombExpOrNot",bombExpOrNot)
    Players[bombExpOrNot[3]][1][0] +=1

    # displaying the local blast
    # global airBlastDisplay
    # airBlastDisplay[bombExpOrNot[0][1], bombExpOrNot[0][0]] = 1
    # print("explodingBomb:32*bombExpOrNot[0][1],32*bombExpOrNot[0][0]",32*bombExpOrNot[0][1],32*bombExpOrNot[0][0])
    airBlast(32*bombExpOrNot[0][1],32*bombExpOrNot[0][0])

    global listOfBombs

    global brokenCrates

    global airBlasts

    # remaining amount of bombs for the current player
    # print("explodingBomb:Players[bombExpOrNot[3]][1][0]", Players[bombExpOrNot[3]][1][0])
    listOfBombs.remove(bombExpOrNot)

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # extend the blast as long as the lengh allow it or if it one crate

    # for bombPosition in listOfBombs:
    # yBomb = bombPosition[0]
    # xBomb = bombPosition[1]
    # print("explodingBomb:bombExpOrNot",bombExpOrNot)
    yBomb = bombExpOrNot[0][0]
    xBomb = bombExpOrNot[0][1]
    # print("explodingBomb:yBomb,xBomb",yBomb,xBomb)

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
                    # print("explodingBomb:[checkingBomb[0][0],checkingBomb[0][1]]",[checkingBomb[0][0],checkingBomb[0][1]])
                    if (np.array_equal([checkingBomb[0][0], checkingBomb[0][1]], [yTmp, xTmp])):
                        # print("issuing:explodingBomb(checkingBomb)")
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

            # print("explodingBomb:[yTmp, xTmp]:",[yTmp, xTmp])

    # print("pathInBlasts\n",pathInBlasts)


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


def isIndexesRangeTileRange(point):
    isInsideIndexRange = False
    if (point[1] >= 0):
        if (point[1] < 16):
            if (point[0] >= 0):
                if (point[0] < 16):
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
        # print("event.type",event.type)
        if event.type == pygame.QUIT:
            pass
        if event.type == pygame.KEYDOWN:
            # print("pygame.K_TAB",pygame.K_TAB)
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
                    # if event.key == pygame.K_6:
                    #     print()
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



end_of_round_time = time.time()

# todo: menu here
# menu: create game/join game/quit

# MAINMENU:
# INIT all the screen
TheMap = np.zeros_like(TheMap)
crateMap = np.zeros_like(TheMap)
# path for cyan player
# line going down
TheMap[1:10,3] = 1
crateMap[1:10,3] = 1
# create a game
TheMap[4,3:7] = 1
crateMap[4,3:7] = 1
# join a game
TheMap[6,3:7] = 1
crateMap[6,3:7] = 1
# quit bomberman
TheMap[8,3:7] = 1
crateMap[8,3:7] = 1

# green lockdown
TheMap[14,19]=1
crateMap[14,19]=1
# cyan lockdown
TheMap[14,0]=1
crateMap[14,0]=1
# blue lockdown
TheMap[0,19]=1
crateMap[0,19]=1



# starting position in the menu
Players[3][0] = [32*3 ,32*1]
# useless players
Players[2][0] = [32*19,32*0]
Players[1][0] = [32*19,32*14]
Players[0][0] = [32*0 ,32*14]

createPointInter = [4,6]
joinPointInter = [6,6]
quitPointInter = [8,6]
interactingPoints = [createPointInter,joinPointInter,quitPointInter]

import struct
def sendOneMulticastAdToLAN():
    print("sendOneMulticastAdToLAN")
    message = b'bomberman-by-not-sure'
    multicast_group = ('192.168.1.255', 5006)
    # Create the datagram socket
    sock_multicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    sock_multicast.settimeout(0)
    # Set the time-to-live for messages to 1 so they do not
    # go past the local network segment.
    ttl = struct.pack('b', 1)
    sock_multicast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    # MY_IP = "192.168.1.99"
    MY_IP = IP_on_LAN
    sock_multicast.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(MY_IP))
    try:
        # while(range(100,0,-1)):
        # Send data to the multicast group
        print('sending {!r}'.format(message))
        sent = sock_multicast.sendto(message, multicast_group)
    finally:
        print('closing socket')
        sock_multicast.close()

runningMenuMain = True
createMenuWhile = False
joinMenuWhile = False

# when createMenuWhile is True
playInLocalWhile = False

createServerTcpIpMenuWhile = False

joinAtcpIpGameMenuWhile = False


enableTcpServerThread = False

listingOfLanHostMenu = False

server_IP_joined = []

lan_listener = 0

# todo:add the TCP Server

# todo:numberOfLocalPlayersMenuWhile = False
# todo:dedicated menu
# todo:normal menu

# Clients information for TCP connect managed by the server
clientIDsWgameState = []

from MultiBN import *

# function used by nothing right now
def manageTCPclientIncomingPackets(incomingData):
    global clientIDsWgameState
    print("manageTCPclientIncomingPackets")
    print("MBN_TCP_CLIENT_JOIN_REQUIRED",MBN_TCP_CLIENT_JOIN_REQUIRED)
    array = (incomingData.decode()).split('|')

    print("array",array)

    if(array[0]==str(MBN_TCP_CLIENT_JOIN_REQUIRED)):
        print("if(array[0]==str(MBN_TCP_CLIENT_JOIN_REQUIRED)):")
        if(clientIDsWgameState.lengh<4):
            print("if (clientIDsWgameState.lengh < 4):")
            pass
    else:
        print()

    pass

pingTimeStart = time.time()

numberOfLocalPlayers = -1

clientSlotKeyboardMapping = []

import socket
# used by the client
tcpClientGameState = [0 for i in range(0, 7)]
def mangageOutGoingTCPclientPackets():
    print("def mangageOutGoingTCPclientPackets():")

    global tcpClientGameState
    print("tcpClientGameState", tcpClientGameState)

    global pingTimeStart

    global clientSlotKeyboardMapping

    TCP_SERVER_IP = "192.168.1.99"

    if(tcpClientGameState[0]==0):
        print("mangageOutGoingTCPclientPackets:if(tcpClientGameState[0]==0):")
        dataTCPclient = str(MBN_TCP_CLIENT_JOIN_REQUIRED)
        print("mangageOutGoingTCPclientPackets:MBN_TCP_CLIENT_JOIN_REQUIRED",MBN_TCP_CLIENT_JOIN_REQUIRED)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server and send data
        sock.connect((TCP_SERVER_IP, 8888))
        sock.sendall(bytes(dataTCPclient, "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(4096), "utf-8")
        print("mangageOutGoingTCPclientPackets:received", received)

        if(int(received.split('|')[0])==MBN_TCP_SERVER_JOIN_ACCEPTED):
            # MBN_TCP_SERVER_JOIN_ACCEPTED
            # Join accepted
            tcpClientGameState[0] = 1

    print("numberOfLocalPlayers",numberOfLocalPlayers)
    if(tcpClientGameState[0] == 1):
        print("mangageOutGoingTCPclientPackets:if(tcpClientGameState[0] == 1):")
        # numberOfLocalPlayers set in joined tcp game menu
        if(numberOfLocalPlayers>=0):
            print("if(numberOfLocalPlayers>=0):")

            if(tcpClientGameState[1] == 0):
                # dataTCPclient = str(MBN_SESSION_TCP_CLIENT_NUMBER_OF_LOCAL_PLAYERS) + "|" + 'lol_ahah'
                dataTCPclient = str(MBN_SESSION_TCP_CLIENT_NUMBER_OF_LOCAL_PLAYERS) + "|" + str(numberOfLocalPlayers)
                print("mangageOutGoingTCPclientPackets:MBN_SESSION_TCP_CLIENT_NUMBER_OF_LOCAL_PLAYERS",MBN_SESSION_TCP_CLIENT_NUMBER_OF_LOCAL_PLAYERS)

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to server and send data
                sock.connect((TCP_SERVER_IP, 8888))
                sock.sendall(bytes(dataTCPclient, "utf-8"))

                # Receive data from the server and shut down
                received = str(sock.recv(4096), "utf-8")
                print("mangageOutGoingTCPclientPackets:received", received)

                tcpClientGameState[1] = 1

                # print("type(received)",type(received))
                # tmpSplit = pickle.loads(received)
                # print("tmpSplit",tmpSplit)
                # if(int(tmpSplit[0])==MBN_SESSION_TCP_SERVER_SLOTS_MAPPING):
                #     clientSlotKeyboardMapping = tmpSplit[1]
                tmpSplit = received.split("|")
                if(int(tmpSplit[0])==MBN_SESSION_TCP_SERVER_SLOTS_MAPPING):
                    tmpClient = [int(tmpSplit[1][1]),int(tmpSplit[1][1+3]),int(tmpSplit[1][1+6]),int(tmpSplit[1][1+9])]
                    clientSlotKeyboardMapping = tmpClient
                    print("clientSlotKeyboardMapping",clientSlotKeyboardMapping)
                    pass


            # todo: change the server side
            # todo: change the tcpClientGameState[0]
            # todo: change the tcpServerGameState[ClientID][0]
        else:
            print("!if(numberOfLocalPlayers>=0):")

    if((time.time()-pingTimeStart)*1000>MBN_CON_UDP_CLIENT_DATA_PING_MS):
        print("if((time.time()-pingTimeStart)*1000>MBN_CON_UDP_CLIENT_DATA_PING_MS):")
        print("(time.time()-pingTimeStart)*1000",(time.time()-pingTimeStart)*1000)
        pingTimeStart = time.time()

        dataTCPclient = str(random.randint(1000,10000))
        print("mangageOutGoingTCPclientPackets:MBN_TCP_CLIENT_JOIN_REQUIRED",MBN_TCP_CLIENT_JOIN_REQUIRED)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server and send data
        sock.connect((TCP_SERVER_IP, 8888))
        sock.sendall(bytes(dataTCPclient, "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(4096), "utf-8")
        print("mangageOutGoingTCPclientPackets:received", received)
        print("ping time",(time.time()-pingTimeStart)*1000,"ms")

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

OnceTCPclient = True

joinedAtcpIpGameMenuWhile = False



currentHostsOnLan = []

import socketserver, threading, time
import socket

# UDP connexion handling
# todo: queuing data that needs processing
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global currentHostsOnLan
        print("ThreadedUDPRequestHandler:handle")
        data = self.request[0].strip()
        socket = self.request[1]
        # print("data",data)
        print("socket.getsockname()",socket.getsockname())
        # (HOST_UDP_server, PORT_UDP_server)
        if(socket.getsockname()[1]==5005):
            print("if(socket.getsockname()[1]==5005):")
            decodedData = pickle.loads(data)
            # print("decodedData[5]",decodedData[5])
            # print("decodedData",decodedData)
            global Players
            if(decodedData[2]=="clientSlotKeyboardMapping"):
                # "clientSlotKeyboardMapping", clientSlotKeyboardMapping
                # print("global Players")
                for slot,i in zip(decodedData[3],range(4)):
                    # print("for slot,i in zip(decodedData[3],range(4)):")
                    if(slot==1):
                        print("Players[i]",Players[i])
                        print("decodedData[1][i]",decodedData[1][i])
                        Players[i] = decodedData[1][i]
            if(decodedData[4]=="listOfBombs"):
                for bomb in decodedData[5]:
                    # done: do a duplicate checking here as well
                    isAlreadyUse = False
                    for b2 in listOfBombs:
                        print("bomb,b2", bomb, b2)
                        if (np.array_equal(bomb[0], b2[0]) == True):
                            print("if (np.array_equal(bomb[0], b2[0]) == True):")
                            isAlreadyUse = True
                        else:
                            print("!if (np.array_equal(bomb[0], b2[0]) == True):")
                    if (isAlreadyUse == False):
                        listOfBombs.append(bomb)
        if(socket.getsockname()[1]==5006):
            print("if(socket.getsockname()[1]==5006):")
            print("currentHostsOnLan",currentHostsOnLan)
            if(data == b'bomberman-by-not-sure'):
                print("b'bomberman-by-not-sure'")
                tmpData, tmpAddress = socket.recvfrom(4096)
                if(tmpAddress[0] not in currentHostsOnLan):
                    currentHostsOnLan.append(tmpAddress[0])
                return
            else:
                # print("!b'bomberman-by-not-sure'")
                pass
            if(listingOfLanHostMenu!=True and joinedAtcpIpGameMenuWhile!=True):
                decodedData = pickle.loads(data)
                print("decodedData",decodedData)
                if(decodedData[0]=="crateMap"):
                    global crateMap
                    crateMap = decodedData[1]
                for slot,i in zip(clientSlotKeyboardMapping,range(4)):
                    if(slot==0):
                        Players[i] = decodedData[3][i]
                if(decodedData[6]=="listOfBombsFromServer"):
                    for b in decodedData[7]:
                        print("decodedData[7]",decodedData[7])
                        isAlreadyUse = False
                        for b2 in listOfBombs:
                            print("b,b2",b,b2)
                            if(np.array_equal(b[0],b2[0])==True):
                                print("if(np.array_equal(b[0],b2[0])==True):")
                                isAlreadyUse = True
                            else:
                                print("!if(np.array_equal(b[0],b2[0])==True):")
                        if(isAlreadyUse==False):
                            print("if(isAlreadyUse==False):")
                            listOfBombs.append([b[0],time.time()-b[1],b[2],b[3]])
                        else:
                            print("if(isAlreadyUse==True):")
                        pass
                        # listOfBombs.append([b[0],time.time()-b[1],b[2],b[3]])
        # print("ThreadedUDPRequestHandler: {}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        # print("threading.activeCount()",threading.activeCount())
        # socket.sendto(data.upper(), self.client_address)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

clientsIPSports = []

# TCP connexion handling
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("ThreadedTCPRequestHandler:handle")
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("self.client_address",self.client_address)
        global clientsIPSports
        print("clientsIPSports",clientsIPSports)
        # print("ThreadedTCPRequestHandler: {} wrote:".format(self.client_address[0]))
        print("self.data",self.data)
        data4function = self.data
        answer = manageTCPserverPackets(data4function,self.client_address)
        print("ThreadedTCPRequestHandler:answer",answer)
        # answering the client
        self.request.sendall(bytes(answer.encode()))
        # # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        print("ThreadedTCPRequestHandler:self.data",self.data)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

while(True):
	# print("runningMenuMain,createMenuWhile,createServerTcpIpMenuWhile,joinAtcpIpGameMenuWhile,joinedAtcpIpGameMenuWhile",runningMenuMain,createMenuWhile,createServerTcpIpMenuWhile,joinAtcpIpGameMenuWhile,joinedAtcpIpGameMenuWhile)
    # print("runningMenuMain,createMenuWhile,createServerTcpIpMenuWhile,joinAtcpIpGameMenuWhile,joinedAtcpIpGameMenuWhile",
     #  runningMenuMain, createMenuWhile, createServerTcpIpMenuWhile, joinAtcpIpGameMenuWhile, joinedAtcpIpGameMenuWhile)
    if(runningMenuMain==True):
        # print("==========================================================")
        pygame.display.set_caption('Bomberman-by-not-sure (Main menu)')
        Controls = keyboardRead()
        ColisionCheckAndMovement()
        if(keyboard.is_pressed('esc')):
            runningMenuMain = False
            print("issuing the esc key")
            pygame.quit()
            quit()
        gameDisplay.fill(gray)
        displayMap()
        displayPlayers()
        displayText("USE ARROWS keys to move around the menu",(display_width / 2), (display_height / 6)+32*0)
        displayText("Create a game",(display_width / 2), (display_height / 6)+32*2)
        displayText("Join a game",(display_width / 2), (display_height / 6)+32*4)
        displayText("Quit bomberman",(display_width / 2), (display_height / 6)+32*6)
        # a bomb mean it is a work in progress
        interactingPoints = [createPointInter, joinPointInter, quitPointInter]
        if(np.array_equal([int(Players[3][0][1]/32),int(Players[3][0][0]/32)],createPointInter)==1):
            print("runningMenuMain:createPointInter",createPointInter)
            # todo: add another submenu about creating game
            runningMenuMain = False
            createMenuWhile = True
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
        if(np.array_equal([int(Players[3][0][1]/32),int(Players[3][0][0]/32)],joinPointInter)==1):
            print("runningMenuMain:joinPointInter",joinPointInter)
            # todo: add another submenu about joining game
            runningMenuMain = False
            createMenuWhile = False
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            # switching to the join menu
            joinAtcpIpGameMenuWhile = True
        if(np.array_equal([int(Players[3][0][1]/32),int(Players[3][0][0]/32)],quitPointInter)==1):
            print("runningMenuMain:quitPointInter",quitPointInter)
            pygame.quit()
            quit()
            pass
    if(createMenuWhile == True):
        # print("==========================================================")
        pygame.display.set_caption('Bomberman-by-not-sure (Create a game)')
        Controls = keyboardRead()
        ColisionCheckAndMovement()
        if(keyboard.is_pressed('esc')):
            runningMenuMain = True
            createMenuWhile = False
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            print("issuing the esc key")
        gameDisplay.fill(gray)
        displayMap()
        displayPlayers()
        displayText("USE ARROWS keys to move around the menu",(display_width / 2), (display_height / 6)+32*0)
        displayText("Play/Create in local",(display_width / 2), (display_height / 6)+32*2)
        displayText("Play/Create on Tcp/Ip",(display_width / 2), (display_height / 6)+32*4)
        displayText("Go back to the main menu",(display_width / 2), (display_height / 6)+32*6)
        # a bomb mean it is a work in progress
        gameDisplay.blit(Tiles[1][5+0],(32*joinPointInter[1],32*joinPointInter[0]))
        interactingPoints = [createPointInter, joinPointInter, quitPointInter]
        if(np.array_equal([int(Players[3][0][1]/32),int(Players[3][0][0]/32)],createPointInter)==1):
            print("createMenuWhile:Local",createPointInter)
            playInLocalWhile = False
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            # newRound in local
            # start the local multiplayer
            newRound()
            # stopping the menu loop
            break
        if(np.array_equal([int(Players[3][0][1]/32),int(Players[3][0][0]/32)],joinPointInter)==1):
            print("createMenuWhile:Tcp/Ip",joinPointInter)
            # todo: add another submenu about joining game
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            createServerTcpIpMenuWhile = True
            createMenuWhile = False
            pass
        if(np.array_equal([int(Players[3][0][1]/32),int(Players[3][0][0]/32)],quitPointInter)==1):
            print("createMenuWhile:Go back to the main menu",quitPointInter)
            runningMenuMain = True
            createMenuWhile = False
            joinMenuWhile = False
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            pass
    # createServerTcpIpMenuWhile
    if(createServerTcpIpMenuWhile == True):
        # print("==========================================================")
        pygame.display.set_caption('Bomberman-by-not-sure (Create a local/internet game)')
        Controls = keyboardRead()
        ColisionCheckAndMovement()
        if(keyboard.is_pressed('esc')):
            runningMenuMain = True
            createMenuWhile = False
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            print("issuing the esc key")
        gameDisplay.fill(gray)
        displayMap()
        displayPlayers()
        displayText("USE ARROWS keys to move around the menu",(display_width / 2), (display_height / 6)+32*0)
        displayText("Dedicated",(display_width / 2), (display_height / 6)+32*2)
        displayText("Normal",(display_width / 2), (display_height / 6)+32*4)
        displayText("Go back to the main menu",(display_width / 2), (display_height / 6)+32*6)
        # a bomb mean it is a work in progress
        gameDisplay.blit(Tiles[1][5+0],(32*createPointInter[1],32*createPointInter[0]))
        interactingPoints = [createPointInter, joinPointInter, quitPointInter]
        if(np.array_equal([int(Players[3][0][1]/32),int(Players[3][0][0]/32)],createPointInter)==1):
            print("createServerTcpIpMenuWhile:dedicated",createPointInter)
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            # start the local multiplayer
            newRound()
            # TCP Server thread enabled
            enableTcpServerThread = True
            # stopping the menu loop
            break
        if(np.array_equal([int(Players[3][0][1]/32),int(Players[3][0][0]/32)],joinPointInter)==1):
            print("createServerTcpIpMenuWhile:Normal",joinPointInter)
            # todo: add another submenu about joining game
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            # start the local multiplayer
            newRound()
            # TCP Server thread enabled
            enableTcpServerThread = True
            break
        if(np.array_equal([int(Players[3][0][1]/32),int(Players[3][0][0]/32)],quitPointInter)==1):
            print("createServerTcpIpMenuWhile:Go back to the main menu",quitPointInter)
            runningMenuMain = True
            createMenuWhile = False
            joinMenuWhile = False
            createServerTcpIpMenuWhile = False
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            pass
    if(joinAtcpIpGameMenuWhile == True):
        # print("if(joinAtcpIpGameMenuWhile == True):")
        pygame.display.set_caption('Bomberman-by-not-sure (Join a Tcp/Ip Game)')

        Controls = keyboardRead()
        ColisionCheckAndMovement()
        if (keyboard.is_pressed('esc')):
            runningMenuMain = False
            print("issuing the esc key")
            pygame.quit()
            quit()
        gameDisplay.fill(gray)
        displayMap()
        displayPlayers()
        displayText("USE ARROWS keys to move around the menu", (display_width / 2), (display_height / 6) + 32 * 0)
        displayText("Local game", (display_width / 2), (display_height / 6) + 32 * 2)
        displayText("Internet game", (display_width / 2), (display_height / 6) + 32 * 4)
        displayText("Go back", (display_width / 2), (display_height / 6) + 32 * 6)
        # a bomb mean it is a work in progress
        gameDisplay.blit(Tiles[1][5 + 0], (32 * joinPointInter[1], 32 * joinPointInter[0]))
        interactingPoints = [createPointInter, joinPointInter, quitPointInter]
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], createPointInter) == 1):
            print("joinAtcpIpGameMenuWhile:createPointInter", createPointInter)
            # todo: add another submenu about creating game
            runningMenuMain = False
            createMenuWhile = False
            joinAtcpIpGameMenuWhile = False
            joinedAtcpIpGameMenuWhile = False
            listingOfLanHostMenu = True
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]

            # line going down
            TheMap[1:15, 3] = 1
            crateMap[1:15, 3] = 1
            # back
            TheMap[14, 3:7] = 1
            crateMap[14, 3:7] = 1
            # masking useless parts
            TheMap[1:13, 4:8] = 0
            crateMap[1:13, 4:8] = 0
        # if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], joinPointInter) == 1):
        #     print("joinAtcpIpGameMenuWhile:joinPointInter", joinPointInter)
        #     # todo: add another submenu about joining game
        #     runningMenuMain = False
        #     createMenuWhile = False
        #     # putting back the cyan player on a neutral spot
        #     Players[3][0] = [32 * 3, 32 * 1]
        #     # switching to the join menu
        #     joinAtcpIpGameMenuWhile = True
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], quitPointInter) == 1):
            print("joinAtcpIpGameMenuWhile:Go back to the main menu",quitPointInter)
            runningMenuMain = True
            createMenuWhile = False
            joinMenuWhile = False
            createServerTcpIpMenuWhile = False
            joinAtcpIpGameMenuWhile = False
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            pass

    if(listingOfLanHostMenu == True):

        print("if(listingOfLanHostMenu == True):")
        pygame.display.set_caption('Bomberman-by-not-sure (listing LANs Game)')

        Controls = keyboardRead()
        ColisionCheckAndMovement()
        if (keyboard.is_pressed('esc')):
            runningMenuMain = False
            print("issuing the esc key")
            pygame.quit()
            quit()
        gameDisplay.fill(gray)
        displayMap()
        displayPlayers()
        displayText("USE ARROWS keys to move around the menu", (display_width / 2), (display_height / 6) + 32 * 0)
        print("listingOfLanHostMenu:currentHostsOnLan",currentHostsOnLan)
        for server,i in zip(currentHostsOnLan,range(len(currentHostsOnLan))):
            print("server",server)
            # displaying the IP
            displayText(server, (display_width / 2), (display_height / 6) + 32 * (2+i))
            # making the path for the server
            TheMap[(4+2*i), 3:7] = 1
            crateMap[(4+2*i), 3:7] = 1
            print("[(4+2*i),6]",[(4+2*i),6])
            print("[int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)]",[int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)])
            # testing if the player is on it
            if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], [(4+2*i),6])):
                print("if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], [(4+2*i),6])):")
                server_IP_joined = server
                print("server_IP_joined",server_IP_joined)
                listingOfLanHostMenu=False
                joinedAtcpIpGameMenuWhile=True
                # putting back the cyan player on a neutral spot
                Players[3][0] = [32 * 3, 32 * 1]
                pass

        if(lan_listener==0):
            if (numberOfLocalPlayers < 0):
                # spectator/players
                print("starting UDP listening on 5006")

                # HOST_UDP_server, PORT_UDP_server = "0.0.0.0", 5006
                HOST_UDP_server, PORT_UDP_server = IP_on_LAN, 5006
                server_udp = ThreadedUDPServer((HOST_UDP_server, PORT_UDP_server), ThreadedUDPRequestHandler)
                server_thread_udp = threading.Thread(target=server_udp.serve_forever)
                server_thread_udp.daemon = True
                try:
                    # servers
                    server_thread_udp.start()
                except (KeyboardInterrupt, SystemExit):
                    server_thread_udp.shutdown()
                    server_thread_udp.server_close()
                    exit()

        lan_listener += 1

        print("listingOfLanHostMenu:currentHostsOnLan", currentHostsOnLan)
        displayText("back", (display_width / 2), (display_height / 6) + 32 * 12)
        interactingPoints = [createPointInter, joinPointInter, quitPointInter]
        # check if any communication are pending or rejected
        # mangageOutGoingTCPclientPackets()
        # if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], createPointInter) == 1):
        #     print("Spectator:createPointInter", createPointInter)
        #     numberOfLocalPlayers = 0
        #     # putting back the cyan player on a neutral spot
        #     Players[3][0] = [32 * 3, 32 * 1]
        #     joinedAtcpIpGameMenuWhile=False
        #     break
        # if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], (quitPointInter[0]+6,quitPointInter[1])) == 1):
        #     print("back_joinedAtcpIpGameMenuWhile:(quitPointInter[0]+6,quitPointInter[1])", (quitPointInter[0]+6,quitPointInter[1]))
        #     # putting back the cyan player on a neutral spot
        #     Players[3][0] = [32 * 3, 32 * 1]
        #     # going back to the previous menu
        #     joinedAtcpIpGameMenuWhile=False
        #     joinAtcpIpGameMenuWhile=True
        #
        #     # closing the path from the previous menu
        #     TheMap[9, 3] = 0
        #     crateMap[9, 3] = 0


    if(joinedAtcpIpGameMenuWhile == True):

        # line going down
        TheMap[1:15, 3] = 1
        crateMap[1:15, 3] = 1
        # 1 player
        TheMap[6, 3:7] = 1
        crateMap[6, 3:7] = 1
        # 2 player
        TheMap[8, 3:7] = 1
        crateMap[8, 3:7] = 1
        # 3 player
        TheMap[10, 3:7] = 1
        crateMap[10, 3:7] = 1
        # 4 player
        TheMap[12, 3:7] = 1
        crateMap[12, 3:7] = 1
        # back
        TheMap[14, 3:7] = 1
        crateMap[14, 3:7] = 1

        # print("if(joinAtcpIpGameMenuWhile == True):")
        pygame.display.set_caption('Bomberman-by-not-sure (Joined a Tcp/Ip Game)')

        Controls = keyboardRead()
        ColisionCheckAndMovement()
        if (keyboard.is_pressed('esc')):
            runningMenuMain = False
            print("issuing the esc key")
            pygame.quit()
            quit()
        gameDisplay.fill(gray)
        displayMap()
        displayPlayers()
        displayText("USE ARROWS keys to move around the menu", (display_width / 2), (display_height / 6) + 32 * 0)
        displayText("Spectator", (display_width / 2), (display_height / 6) + 32 * 2)
        displayText("1 player", (display_width / 2), (display_height / 6) + 32 * 4)
        displayText("2 player", (display_width / 2), (display_height / 6) + 32 * 6)
        displayText("3 player", (display_width / 2), (display_height / 6) + 32 * 8)
        displayText("4 player", (display_width / 2), (display_height / 6) + 32 * 10)
        displayText("back", (display_width / 2), (display_height / 6) + 32 * 12)
        # a bomb mean it is a work in progress
        gameDisplay.blit(Tiles[1][5 + 0], (32 * joinPointInter[1], 32 * (joinPointInter[0]+0)))
        gameDisplay.blit(Tiles[1][5 + 0], (32 * joinPointInter[1], 32 * (joinPointInter[0]+2)))
        gameDisplay.blit(Tiles[1][5 + 0], (32 * joinPointInter[1], 32 * (joinPointInter[0]+4)))
        gameDisplay.blit(Tiles[1][5 + 0], (32 * joinPointInter[1], 32 * (joinPointInter[0]+6)))
        interactingPoints = [createPointInter, joinPointInter, quitPointInter]
        # check if any communication are pending or rejected
        mangageOutGoingTCPclientPackets()
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], createPointInter) == 1):
            print("Spectator:createPointInter", createPointInter)
            numberOfLocalPlayers = 0
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            joinedAtcpIpGameMenuWhile=False
            break
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], joinPointInter) == 1):
            print("local1player:createPointInter", createPointInter)
            numberOfLocalPlayers = 1
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            joinedAtcpIpGameMenuWhile=False
            print()
            break
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], quitPointInter) == 1):
            print("local2player:createPointInter", createPointInter)
            numberOfLocalPlayers = 2
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            joinedAtcpIpGameMenuWhile=False
            break
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], (quitPointInter[0]+2,quitPointInter[1])) == 1):
            print("local3player:(quitPointInter[0]+2,quitPointInter[1])", (quitPointInter[0]+2,quitPointInter[1]))
            numberOfLocalPlayers = 3
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            joinedAtcpIpGameMenuWhile=False
            break
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], (quitPointInter[0]+4,quitPointInter[1])) == 1):
            print("local4player:(quitPointInter[0]+4,quitPointInter[1])", (quitPointInter[0]+4,quitPointInter[1]))
            numberOfLocalPlayers = 4
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            joinedAtcpIpGameMenuWhile=False
            break
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], (quitPointInter[0]+6,quitPointInter[1])) == 1):
            print("back_joinedAtcpIpGameMenuWhile:(quitPointInter[0]+6,quitPointInter[1])", (quitPointInter[0]+6,quitPointInter[1]))
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            # going back to the previous menu
            joinedAtcpIpGameMenuWhile=False
            joinAtcpIpGameMenuWhile=True

            # closing the path from the previous menu
            TheMap[9, 3] = 0
            crateMap[9, 3] = 0


    pygame.display.update()
    # print('time:',str(time.time()-st_time))
    clock.tick(60)
    st_time = time.time()

# number of slots left on server
slotsLeftOnServer = 4
# slotsMappingForPlayersControl
slotsMappingForPlayersControl = [0 for i in range(4)]
# used by ThreadedTCPRequestHandler
def manageTCPserverPackets(incomingData,client_addr):
    # Clients informations for TCP connect managed by the server
    # [clientID,IP,port,state of the game]
    global clientIDsWgameState
    # adding the infos to count down
    global slotsLeftOnServer
    global clientsIPSports
    print("manageTCPserverPackets")
    print("manageTCPserverPackets:MBN_TCP_CLIENT_JOIN_REQUIRED", MBN_TCP_CLIENT_JOIN_REQUIRED)
    array = (incomingData.decode()).split('|')
    print("manageTCPserverPackets:array", array)

    if(array[0]==str(MBN_TCP_CLIENT_JOIN_REQUIRED)):
        print("manageTCPserverPackets:if(array[0]==str(MBN_TCP_CLIENT_JOIN_REQUIRED)):")
        print("clientIDsWgameState",clientIDsWgameState)
        if(clientIDsWgameState!=[]):
            if(len(clientIDsWgameState)>=4):
                print("manageTCPserverPackets:if(len(clientIDsWgameState)>=4):")
                print("return MBN_TCP_SERVER_JOIN_REFUSED")
                return str(MBN_TCP_SERVER_JOIN_REFUSED)
                pass
            else:
                print("!if(len(clientIDsWgameState)>=4):")
                clientID = len(clientIDsWgameState)
                clientIDsWgameState.append([clientID,client_addr])
                clientsIPSports.append([client_addr[0], client_addr[1]])
                print("return MBN_TCP_SERVER_JOIN_ACCEPTED")
                return str(MBN_TCP_SERVER_JOIN_ACCEPTED) + "|" + str(clientID) + "|" + str(slotsLeftOnServer+1)
        else:
            print("!if(clientIDsWgameState!=[]):")
            clientID = len(clientIDsWgameState)
            clientIDsWgameState.append([clientID,client_addr])
            clientsIPSports.append([client_addr[0], client_addr[1]])
            print("return MBN_TCP_SERVER_JOIN_ACCEPTED")
            return str(MBN_TCP_SERVER_JOIN_ACCEPTED) + "|" + str(clientID) + "|" + str(slotsLeftOnServer+1)
            pass
    else:
        print("manageTCPserverPackets",array[0],str(MBN_TCP_CLIENT_JOIN_REQUIRED))

    if(array[0]==str(MBN_SESSION_TCP_CLIENT_NUMBER_OF_LOCAL_PLAYERS)):
        print("manageTCPserverPackets:MBN_SESSION_TCP_CLIENT_NUMBER_OF_LOCAL_PLAYERS")
        print("manageTCPserverPackets:array[1]",array[1])
        if(int(array[1])>slotsLeftOnServer):
            # client ask for too many slots, answer the number available, it need to adapt its menu
            print("str(MBN_SESSION_TCP_SERVER_NUMBER_OF_AVAILABLE_PLAYERS_SLOTS)  + | + str(slotsLeftOnServer)")
            return str(MBN_SESSION_TCP_SERVER_NUMBER_OF_AVAILABLE_PLAYERS_SLOTS)  + "|" + str(slotsLeftOnServer)
        else:
            if(int(array[1])==0):
                # do nothing
                return str(MBN_SESSION_TCP_SERVER_SLOTS_MAPPING) + "|" + str(slotsMappingForPlayersControl)
            else:
                # array[1] is != 0
                tmpSlotMapping = [0 for i in range(4)]

                print("tmpSlotMapping",tmpSlotMapping)

                # # for test purpose
                # slotsLeftOnServer = 3

                # # generating a pre-mask for the final results as shown above
                for iSlot in range(int(slotsLeftOnServer), 0, -1):
                    # single client is ok
                    # work 4 with slotsLeftOnServer 4:ok
                    # work 3 with slotsLeftOnServer 4:ok
                    # work 2 with slotsLeftOnServer 4:ok
                    # several clients
                    # work 3 with slotsLeftOnServer 4 and work 1 with slotsLeftOnServer 4 ?
                    # for iSlot in range(4 - int(slotsLeftOnServer), int(slotsLeftOnServer), 1):
                    # enabling the mask starting from the end
                    print("str(iSlot)", str(iSlot))
                    tmpSlotMapping[-iSlot] = 1
                    pass
                print("tmpSlotMapping1",tmpSlotMapping)

                i = 0
                for j in tmpSlotMapping:
                    if(i>=int(array[1])):
                        tmpSlotMapping[i] = 0
                    if (j==1):
                        i+=1
                print("tmpSlotMapping2",tmpSlotMapping)

                slotsLeftOnServer -= int(array[1])

                # todo: send the client a random number which would be used identify who is speaking to the server
                # to make that client are not poking around the slots mapping control

                print("return str(MBN_SESSION_TCP_SERVER_SLOTS_MAPPING) + | + str(tmpSlotMapping)")
                return str(MBN_SESSION_TCP_SERVER_SLOTS_MAPPING) + "|" + str(tmpSlotMapping)
                # tmpPickle =  pickle.dumps([MBN_SESSION_TCP_SERVER_SLOTS_MAPPING,tmpSlotMapping])
                # return tmpPickle
            print("manageTCPserverPackets:slotsMappingForPlayersControl",slotsMappingForPlayersControl)
            # return str(slotsLeftOnServer)
            pass
    print("manageTCPserverPackets:slotsLeftOnServer",slotsLeftOnServer)

    # ping feature
    if(int(array[0])>=1000):
        print("manageTCPserverPackets:ping feature")
        return str(int(array[0])+1)
        pass

    return str([])
    pass


if __name__ == "__main__":
    if(enableTcpServerThread==True):
        # HOST_TCP, PORT_TCP = "0.0.0.0", 8888
        HOST_TCP, PORT_TCP = IP_on_LAN, 8888
        server_tcp = ThreadedTCPServer((HOST_TCP, PORT_TCP), ThreadedTCPRequestHandler)
        server_thread_tcp = threading.Thread(target=server_tcp.serve_forever)
        server_thread_tcp.daemon = True

        try:
            # servers
            server_thread_tcp.start()
            print("server_thread_tcp.start()")

        except (KeyboardInterrupt, SystemExit):
            server_thread_tcp.shutdown()
            server_thread_tcp.server_close()
            exit()

# clean the menu on the server side
newRound()

if (numberOfLocalPlayers < 0):
    # numberOfLocalPlayers = -1
    # is hosting a game
    pygame.display.set_caption('Bomberman-by-not-sure (Host of Tcp/Ip Game)')

    # HOST_UDP_server, PORT_UDP_server = "0.0.0.0", 5005
    HOST_UDP_server, PORT_UDP_server = IP_on_LAN, 5005
    server_udp = ThreadedUDPServer((HOST_UDP_server, PORT_UDP_server), ThreadedUDPRequestHandler)
    server_thread_udp = threading.Thread(target=server_udp.serve_forever)
    server_thread_udp.daemon = True
    try:
        # servers
        server_thread_udp.start()
    except (KeyboardInterrupt, SystemExit):
        server_thread_udp.shutdown()
        server_thread_udp.server_close()
        exit()
else:
    pass
    # # spectator/players
    # pygame.display.set_caption('Bomberman-by-not-sure (Client of Tcp/Ip Game)')
    #
    # # HOST_UDP_server, PORT_UDP_server = "0.0.0.0", 5006
    # HOST_UDP_server, PORT_UDP_server = IP_on_LAN, 5006
    # server_udp = ThreadedUDPServer((HOST_UDP_server, PORT_UDP_server), ThreadedUDPRequestHandler)
    # server_thread_udp = threading.Thread(target=server_udp.serve_forever)
    # server_thread_udp.daemon = True
    # try:
    #     # servers
    #     server_thread_udp.start()
    # except (KeyboardInterrupt, SystemExit):
    #     server_thread_udp.shutdown()
    #     server_thread_udp.server_close()
    #     exit()

last_ad_multicast = time.time()

while(runningMain):
    # # print("==========================================================")
    # # if the user joined a tcp server
    # # todo: check server_gist.py for design pattern
    # # todo: no blocking UDP sending
    # # todo: time out and refusal management

    if (numberOfLocalPlayers < 0):
        # # numberOfLocalPlayers = -1
        # # is hosting a game
        # print("!if(numberOfLocalPlayers<0):")
        for client in clientsIPSports:
            print("hosting")
            # UDP_IP_CLIENT = "127.0.0.1"
            # UDP_IP_CLIENT = IP_on_LAN
            UDP_IP_CLIENT = client[0]
            UDP_PORT_CLIENT = 5006
            if(listOfBombs!=[]):
                print("listOfBombs",listOfBombs)
            listOfBombsFromServer = [ [ b[0],time.time()-b[1],b[2],b[3] ] for b in listOfBombs]
            if(listOfBombsFromServer!=[]):
                print("listOfBombsFromServer",listOfBombsFromServer)
            MESSAGE = pickle.dumps(["crateMap",crateMap,"Players",Players,
                                    "clientSlotKeyboardMapping",clientSlotKeyboardMapping,
                                    "listOfBombsFromServer",listOfBombsFromServer])
            MESSAGE_bytes = MESSAGE
            # print("client message:", MESSAGE_bytes)

            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP
            sock.setblocking(False)
            # print("len(MESSAGE_bytes)",len(MESSAGE_bytes))
            sock.sendto(MESSAGE_bytes, (UDP_IP_CLIENT, UDP_PORT_CLIENT))

        if ((time.time() - last_ad_multicast) * 1000 > 1000):
            sendOneMulticastAdToLAN()
            last_ad_multicast = time.time()

    else:
        # check if any communication are pending or rejected
        mangageOutGoingTCPclientPackets()
        # spectator/players
        # print("!if(numberOfLocalPlayers<0):")
        print("spectator/players")
        # UDP_IP_CLIENT = "127.0.0.1"
        # UDP_IP_CLIENT = IP_on_LAN
        UDP_IP_CLIENT = server_IP_joined
        UDP_PORT_CLIENT = 5005
        MESSAGE = pickle.dumps(["Players",Players,"clientSlotKeyboardMapping",clientSlotKeyboardMapping,"listOfBombs",listOfBombs])
        MESSAGE_bytes = MESSAGE
        # print("client message:", MESSAGE_bytes)

        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.setblocking(False)
        sock.sendto(MESSAGE_bytes, (UDP_IP_CLIENT, UDP_PORT_CLIENT))

    print("clientSlotKeyboardMapping",clientSlotKeyboardMapping)

    print("runningMain:currentHostsOnLan",currentHostsOnLan)

    Controls = keyboardRead()

    ColisionCheckAndMovement()

    if(keyboard.is_pressed('esc')):
        runningMain = False
        print("issuing the esc key")

    gameDisplay.fill(gray)

    displayCrates()
    displayMap()
    displayBombs()
    # print("brokenCrates",brokenCrates)
    displayBrokenCratesAndUpdateCollision()
    playersPickupsItems()
    displayAirBlasts()
    # done:Score display is slow
    if(boolDisplayScores == True):
        print("displayScores()")
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
    print('time:',str(time.time()-st_time))
    clock.tick(60)
    st_time = time.time()

pygame.quit()
quit()

# todo: done for now: add window titles change to the menus
# todo: queuing data that needs processing ?

# done: add a submenu on the join a game
# done: submenu join local game
# done: submenu join game internet
# done: players's position send to the host
# todo: removing the bomb from the tcp/ip hosting in the menu
# todo: add multicast advertissement on the local network (when hosting a game)
# todo: host the TCP/IP game as the local LAN IP not localhost
# todo: implement a dedicated mode for TCP/IP game
# todo: allow the host to play as client in non-dedicated mode TCP/IP
# todo: add a design doc
# done: do a server list for the lan games
# done: dispatch the packets to every clients
# done: do a proper keyboard binding with slots by the server side
# done: add an auto-updater (for main) to get the new script on each tests' computers

# todo: add the client side on join a game
# todo: add the server side clients' players management
# todo: add the server search on local
# todo: add a server listing onto the internet games
# Not done: add a timeout on tcp and udp thread (receiving/sending)
