import pygame

import keyboard
import numpy as np

import time
import itertools

import random

# image processing and skin loading
from PIL import Image

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
        if(listOfBombs!=[]):
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

runningMenuMain = True
createMenuWhile = False
joinMenuWhile = False

# when createMenuWhile is True
playInLocalWhile = False

createServerTcpIpMenuWhile = False

joinAtcpIpGameMenuWhile = False


enableTcpServerThread = False

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

import socket
tcpClientGameState = [0 for i in range(0, 7)]
def mangageOutGoingTCPclientPackets():
    print("def mangageOutGoingTCPclientPackets():")

    global tcpClientGameState
    print("tcpClientGameState", tcpClientGameState)

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

        # Join accepted
        tcpClientGameState[0] = 1

        # todo: change the server side
        # todo: change the tcpClientGameState[0]
        # todo: change the tcpServerGameState[ClientID][0]

    pass

OnceTCPclient = True

while(True):
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
        print("if(joinAtcpIpGameMenuWhile == True):")
        time.sleep(0.25)
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
        displayText("Internet a game", (display_width / 2), (display_height / 6) + 32 * 4)
        displayText("Go back", (display_width / 2), (display_height / 6) + 32 * 6)
        # a bomb mean it is a work in progress
        gameDisplay.blit(Tiles[1][5 + 0], (32 * joinPointInter[1], 32 * joinPointInter[0]))
        interactingPoints = [createPointInter, joinPointInter, quitPointInter]
        # check if any communication are pending or rejected
        mangageOutGoingTCPclientPackets()
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], createPointInter) == 1):
            print("runningMenuMain:createPointInter", createPointInter)
            # todo: add another submenu about creating game
            runningMenuMain = False
            createMenuWhile = True
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
        # if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], joinPointInter) == 1):
        #     print("runningMenuMain:joinPointInter", joinPointInter)
        #     # todo: add another submenu about joining game
        #     runningMenuMain = False
        #     createMenuWhile = False
        #     # putting back the cyan player on a neutral spot
        #     Players[3][0] = [32 * 3, 32 * 1]
        #     # switching to the join menu
        #     joinAtcpIpGameMenuWhile = True
        if (np.array_equal([int(Players[3][0][1] / 32), int(Players[3][0][0] / 32)], quitPointInter) == 1):
            print("createServerTcpIpMenuWhile:Go back to the main menu",quitPointInter)
            runningMenuMain = True
            createMenuWhile = False
            joinMenuWhile = False
            createServerTcpIpMenuWhile = False
            joinAtcpIpGameMenuWhile = False
            # putting back the cyan player on a neutral spot
            Players[3][0] = [32 * 3, 32 * 1]
            pass


        # # for debugging purposes
        # newRound()
        # break
    else:
        print("!if(joinAtcpIpGameMenuWhile == True):")

    pygame.display.update()
    # print('time:',str(time.time()-st_time))
    clock.tick(10)
    st_time = time.time()

# testing lines
# clientIDsWgameState.append('lol')
# clientIDsWgameState.append('lol')
# clientIDsWgameState.append('lol')
# clientIDsWgameState.append('lol')
# clientIDsWgameState.append('lol')

# used by ThreadedTCPRequestHandler
def manageTCPserverPackets(incomingData,client_addr):
    # Clients informations for TCP connect managed by the server
    # [clientID,IP,port,state of the game]
    global clientIDsWgameState
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
                print("return MBN_TCP_SERVER_JOIN_ACCEPTED")
                return str(MBN_TCP_SERVER_JOIN_ACCEPTED) + "|" + str(clientID)
        else:
            print("!if(clientIDsWgameState!=[]):")
            clientID = len(clientIDsWgameState)
            clientIDsWgameState.append([clientID,client_addr])
            print("return MBN_TCP_SERVER_JOIN_ACCEPTED")
            return str(MBN_TCP_SERVER_JOIN_ACCEPTED) + "|" + str(clientID)
            pass
    else:
        print("manageTCPserverPackets",array[0],str(MBN_TCP_CLIENT_JOIN_REQUIRED))

    return str([])
    pass

import socketserver, threading, time
# TCP connexion handling
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("ThreadedTCPRequestHandler")
        # print("ThreadedTCPRequestHandler: {} wrote:".format(self.client_address[0]))
        print("self.data",self.data)
        data4function = self.data
        answer = manageTCPserverPackets(data4function,self.client_address)
        print("ThreadedTCPRequestHandler:answer",answer)
        # answering the client
        self.request.sendall(bytes(answer.encode()))
        # # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        print("ThreadedTCPRequestHandler:data",data)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    if(enableTcpServerThread==True):
        HOST_TCP, PORT_TCP = "0.0.0.0", 8888
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

    import socket

    # if(joinAtcpIpGameMenuWhile == True):
    #     print('"if __name__ == "__main__":','if(joinAtcpIpGameMenuWhile == True):')
    #     print("TCP Client")
    #     commAsTCPclient()
        # dataTCPclient = " Lolilol"
        #
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #
        # # Connect to server and send data
        # sock.connect(("192.168.1.99", 8888))
        # sock.sendall(bytes(dataTCPclient, "utf-8"))
        #
        # # Receive data from the server and shut down
        # received = str(sock.recv(4096), "utf-8")
        # print("received",received)
        # pass


while(runningMain):
    time.sleep(1)
    # print("==========================================================")
    Controls = keyboardRead()

    ColisionCheckAndMovement()

    if(keyboard.is_pressed('esc')):
        runningMain = False
        print("issuing the esc key")

    gameDisplay.fill(gray)
    # crate(0,0)

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
    # print('time:',str(time.time()-st_time))
    clock.tick(60)
    st_time = time.time()
    # print('lol')

pygame.quit()
quit()

# todo: done for now: add window titles change to the menus
# todo: queuing data that needs processing ?

# done: add a submenu on the join a game
# todo: submenu join a local game
# todo: submenu join a game internet
# todo: add the client side on join a game
# todo: add the server search on local
# todo: add a server listing onto the internet games
#