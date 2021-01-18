# Library made and documented in November 2020 by Matthew (Angelo) Kreitzer 
# This library mainly used for the following purposes:
# 1- Generate phase portraits for two state FBCAs. (As documented by https://atrium.lib.uoguelph.ca/xmlui/handle/10214/21316)
# These phase portraits document all possible level-maps generated by two dimensional systems.
# 2- Generation of linear morphs for high state FBCAs. (As documented by doi: 10.1109/CIG.2019.8847947. )
# These morphs attempt to combine two behaviourally distinct FBCAs utilizing a line in n^2 dimensional matrix space
# In addition, classification of these morphs is done by regula falsi and a morph portrait (to be documented)
# NOT ADDED YET
# 3- Generation of crisscrossing to generate higher state FBCA (to be documented)


# Standard python library imports
from PIL import Image #for visualization through image generation
import random # for L_0 generation
import math # for a small number of operations
import numpy # for a small number of operations
import os # for folder/file gen
import time # for debugging

# Global inits

# The below determine F,g,n and if the processes used will be visualized through images
numOfGens=40 #number of generations (g)
numOfStates=2 #number of states (n) [defined till 10]
numOfNeighbours=4 #used for fingerprinter

# F
# F is defined as a torus and needs parameters to define this
CALength=100 #Length of torus (related to thickness of the torus) [for dB method use 5]
CAWidth=100 #Width of torus (related to radius of the torus) [for dB method use 4]
useMinMap=0 #honestly, something I have to fix
# F's connectivity is arbitrary. It is assumed each cell has the same connectivity.
# To represent the connectivity, a list of touples representing the x and y offset is needed
# The default is Von Neumann and is defined below
neighbours=[]
neighbours.append((0,1))#top (1 up)
neighbours.append((0,-1))#bot (1 down)
neighbours.append((-1,0))#left (1 left)
neighbours.append((1,0))#right (1 right)

# Visualization parameters
useImages=0 #checks if you want images  
finalImage=1 #checks if you want the final image of a generated FBCA



## DATA STRUCTURES ## 

# Cell data structure #
# By defintion a FBCA cell has:
# # A cell has a state (being some natural number 0->n)
# # A cell has a score (detailed in https://atrium.lib.uoguelph.ca/xmlui/handle/10214/21316 )
class CACell:
    state=0
    score=0

# FBCA data structure #
# By defintion an FBCA has:
# # An FBCA has a final array of states known as L_g. (this normally is a two dimensional array)
# # # Since level generation uses this to make its maps it is known as the FBCA's levelmap
# # An FBCA is normally defined by S, its score matrix. 
# # # Normally g,n,L_0 and F also define an FBCA but since these are globally defined they are not considered.  
# # The 'type' is recorded (if known) for an FBCA through its behaviour number
class Fbca:
    levelMap=[]
    scoreMatrix=[]
    behaviourNum=0

# Fingerprint data structure #
# This contains the sorted set of inequalities that determine behavioural equivlance #
# The parts are named as such to mirror FBCAs #
class fPrint:
    fPrint=[]
    scoreMatrix=[]
    behaviourNum=-1

## FUNCTIONS ##


## GENERAL ## ## GENERAL ## ## GENERAL ##
## GENERAL ## ## GENERAL ## ## GENERAL ##

# State to Colour converter #
### Input: state (as an int)
### Output: RGB touple
# Notes:
# When visualize through images, each state is given a colour. All colours are arbitrary with one exception:
# # Some evolutionary computation attempts to force certain behaviours by constraning the first state 
# # This was done to preserve 'open space' and as such the first state is always white.
def colourConvert(x):
    return {
        0: (255,255,255),
        1: (0,0,0),
        2: (0,255,0),
        3: (0,0,255),
        4: (255,0,0),
        5: (51,255,255),
        6: (0,255,255),
        7: (255,69,0),
        8: (0,102,0),
        9: (153,0,153),
        10: (255,255,51),
    }[x]    

# Copying function #
### Input: A list full of CACells
### Output: Another list full cells with the same states as the input
# Notes:
# The standard copy method loses data for a list of classes.
def copyOver(CAMapInit):
    CAMap=[]
    for x in range(0,CALength):
        holder=[]
        for y in range(0,CAWidth):
            holder.append(CACell())
            holder[y].state=CAMapInit[x][y].state
        CAMap.append(holder)
    return(CAMap)

#This function parses the text data generated by 
def convTextListToList(listAsText):
    importantStuff=[]
    importantStuff=listAsText.split(",")
    importantStuff[0]=importantStuff[0].split("[")[1]
    l=len(importantStuff)
    importantStuff[l-1]=importantStuff[l-1].split("]")[0]
    importantStuff=[float(i) for i in importantStuff]
    return(importantStuff)

# Copying function 2#
### Input: A list
### Output: Another list with the same contents of the input
# Notes:
# Out of fear of losing data, I made my own copying function.
def copyList(listInit):
    holder=[]
    for x in listInit:
        holder.append(x)
    return(holder)

# Gets the ascending compositions of the integer partitioning 
# From http://jeromekelleher.net/tag/integer-partitions.html  
# I need to study this and possibly remake my own
def ascIntPart(n):
    a = [0 for i in range(n + 1)]
    k = 1
    a[1] = n
    while k != 0:
        x = a[k - 1] + 1
        y = a[k] - 1
        k -= 1
        while x <= y:
            a[k] = x
            y -= x
            k += 1
        a[k] = x + y
        yield a[:k + 1]


# Folder generation #
### Input: Name of a folder we want to make
### Output: True (1) or False (0) if folder is made 
def makeFolder(folderName):
    try: 
        os.makedirs(folderName)
        return(1)
    except:
        return(0)

# Image generation method #
### Input: L_n (2d list of CACell with states), n, folder name, 
### Output: An image file
# Notes:
# I have no idea what an image file is
def genIm(CAMap,n,directory=os.getcwd(),quantifer="giveName"):
    im= Image.new('RGB', (CALength, CAWidth))
    for x in range(CALength):
        for y in range(CAWidth):
            im.putpixel((x,y),colourConvert(CAMap[x][y].state))
    im.save(f"{directory}{quantifer} {str(n)}.png")
    return(im)

# Generate an rgb colour based upon the enumerated index of an object
### Input: the index, the object 
### Output: a touple for rgb
# Notes:
# # The function takes the index (where it is effectively) and the object (to find its lengths) 
# # It then generates a colour (up to 255*12) possible distinct combinations
def getBehCol(idx, thing):
    imageColourStep=(255*10)/(len(thing))
    colourVal=int(idx*imageColourStep)

    if (colourVal-255<0): # 1
        r = colourVal
        g=0
        b=0
    else:
        colourVal-=255
        if (colourVal-255<0): # 2
            r=0
            g = colourVal
            b=0
        else:
            colourVal-=255
            if (colourVal-255<0): # 3
                r = 0
                g=0
                b = colourVal
            else:
                colourVal-=255
                if (colourVal-255<0): # 4
                    r = colourVal
                    g = 255 
                    b = 0
                else: 
                    colourVal-=255
                    if (colourVal-255<0): # 5
                        r = colourVal
                        g = 0 
                        b = 255
                    else:
                        colourVal-=255
                        if (colourVal-255<0): # 6
                            r = 255 
                            g = colourVal
                            b = 0
                        else:
                            colourVal-=255
                            if (colourVal-255<0): # 7
                                r = 0
                                g = colourVal
                                b = 255
                            else:
                                colourVal-=255
                                if (colourVal-255<0): # 8
                                    r = 255
                                    g = 0
                                    b = colourVal
                                else: 
                                    colourVal-=255
                                    if (colourVal-255<0): # 9
                                        r = 0
                                        g = 255
                                        b = colourVal
                                    else:
                                        colourVal-=255
                                        if (colourVal-255<0): # 10
                                            r = colourVal
                                            g = 255
                                            b = 255
                                        else:
                                            colourVal-=255
                                            if (colourVal-255<0): # 11
                                                r = 255
                                                g = colourVal
                                                b = 255
                                            else:
                                                colourVal-=255
                                                if (colourVal-255<0): # 12
                                                    r = 255
                                                    g = 255
                                                    b = colourVal
                                                else:
                                                    r = 255
                                                    g = 255
                                                    b = 255
    return((r,g,b))

## FBCA ## ## FBCA ## ## FBCA ##
## FBCA ## ## FBCA ## ## FBCA ##

# L_0 generation #
### Input: A list full of CACells (representing an empty FBCA)
### Output: A list full of CACells with a pseudo-random collection of states
# Notes:
# L_0s are prefered to be constant for checking weak behavioural equivlance. 
# To do this, simply call initCA once and use the copyOver function (other methods lead to data loss) 
def initCA(CAMap):
    #Fills in downward stripes as we interate x then y
    for x in range(0,CALength):
        holder=[] #downward column at the x value
        for y in range(0,CAWidth):
            holder.append(CACell()) #adds in a cell and randomizes its state
            holder[y].state=random.randint(0,numOfStates-1)
        CAMap.append(holder)
    if(useMinMap==1):
        CAMap[0][0].state=1;CAMap[1][0].state=1;CAMap[2][0].state=0;CAMap[3][0].state=0;CAMap[4][0].state=1
        CAMap[0][1].state=1;CAMap[1][1].state=0;CAMap[2][1].state=0;CAMap[3][1].state=0;CAMap[4][1].state=1
        CAMap[0][2].state=0;CAMap[1][2].state=1;CAMap[2][2].state=0;CAMap[3][2].state=1;CAMap[4][2].state=1
        CAMap[0][3].state=1;CAMap[1][3].state=0;CAMap[2][3].state=0;CAMap[3][3].state=0;CAMap[4][3].state=1
    return(CAMap)

# Generation of FBCA #
##Input: Score matrix (as a one dimensional list), directory, L_0 and a quantifer
##Output: L_g for the system, if visualized L will be generated in a folder named by the quantifer.
# Notes:
# Since F,g,L_0,n are all constant, they are not needed for the generate FBCA function.
# The global variables useImages and finalImage dictate if visual records are kept for generated FBCAs
# The visual records come as a gif and L_g (I am having difficulty making it just a bunch of single images)
def generateFBCA(scoreMatrix,d,CAMapInit,quantifer):
    gif=[];CAMap=[];CAMap=copyOver(CAMapInit)
    if (useImages==1) or (finalImage==1):
        d=f"{d}/{quantifer}/"
    makeFolder(d)
    for n in range(numOfGens):
        if (useImages==1):
            gif.append(genIm(CAMap,numOfGens,d,quantifer))
        CAMap=updateMap(CAMap,scoreMatrix)
    if (finalImage==1):
        gif.append(genIm(CAMap,numOfGens,d,quantifer))
        gif[0].save(f"{d}{quantifer}.gif",save_all=True,append_images=gif[1:],optimize=False,duration=100,loop=0)
    return(CAMap)

# FBCA Updater #
### Input: An L_n (2d list of CACells), A score matrix (stored as a 1d list)
### Output: L_(n+1) (2d list of CACells)
# Notes:
# The update is done in 3 steps:
# # Assigns each cell its score
# # Generates a copy of the L_g
# # Updates the states of the copy by taking the highest score state of a cells neighbourhood
# # The copy is then returned
# # The default neighbourhood is Von Neumann and is defined by the neighbours function 
def updateMap(CAMap,scoreMatrix):

    for x in range(0,CALength):
        for y in range(0,CAWidth):
            #Need to get score from center square and its neighbours.
            row = CAMap[x][y].state*numOfStates #the center colour determines the row of the score matrix used 
            #new method to save a small amount of computation
            col0=CAMap[(x+neighbours[0][0])%CALength][(y+neighbours[0][1])%CAWidth].state 
            col1=CAMap[(x+neighbours[1][0])%CALength][(y+neighbours[1][1])%CAWidth].state 
            col2=CAMap[(x+neighbours[2][0])%CALength][(y+neighbours[2][1])%CAWidth].state 
            col3=CAMap[(x+neighbours[3][0])%CALength][(y+neighbours[3][1])%CAWidth].state
            CAMap[x][y].score=scoreMatrix[row+col0]+scoreMatrix[row+col1]+scoreMatrix[row+col2]+scoreMatrix[row+col3]
    #start by copying the map
    CAMapCopy=copyOver(CAMap)
    #for every cell, find the highest score among neighbours
    for x in range(0,CALength):
        for y in range(0,CAWidth):
            #NOTE: We give priority to the center square on ties. Priority continues up with the last defined neighbour to have the worst priority
            bigScore=0;bigScore=CAMap[x][y].score
            #compares neighbours scores, reassigning bigScore and state if someone is bigger
            for z in neighbours:
                if(bigScore<CAMap[(x+z[0])%CALength][(y+z[1])%CAWidth].score):
                    bigScore=CAMap[(x+z[0])%CALength][(y+z[1])%CAWidth].score
                    CAMapCopy[x][y].state=CAMap[(x+z[0])%CALength][(y+z[1])%CAWidth].state
    return(CAMapCopy)


## SCORE MATRIX ## ## SCORE MATRIX ## ## SCORE MATRIX ##
## SCORE MATRIX ## ## SCORE MATRIX ## ## SCORE MATRIX ##

# Generate score matrix from a morph #
### Input: Score matrix 1 (1d list), Score matrix 2 (1d list), lambda (float)
### Output: Score matrix lambda
# Notes:
# Uses general equation of a convex set: lambda*sM1 + (1-lambda)*sM2 = sMLambda
def genMorphSM(sM1,sM2,lamb):
    sMNew=[]
    for i in range(len(sM1)):
        sMNew.append(lamb*sM2[i]+(1-lamb)*sM1[i])
    return(sMNew)

## BEHAVIOUR ## ## BEHAVIOUR ## ## BEHAVIOUR ##
## BEHAVIOUR ## ## BEHAVIOUR ## ## BEHAVIOUR ##

# Weak behavioural equivalence detector through L_g comparison #
##Input: Two L_gs represented as a lists of cells. 
##Output: True (1) or False (0) if weakly behaviourally equivalent 
# Notes:
# It is assumed that both L_gs are generated using the same F,g,L_0,n.
# Because of this, if all cells of the L_g's have the same state, they are weakly behaviourally equivalent.  
def compareLs(lg1,lg2):
    isSame=1;x=0;y=0
    while (x < CALength) and (isSame==1):
        while (y < CAWidth) and (isSame==1):
            if (lg1.lG[x][y].state!=lg2.lG[x][y].state):
                isSame=0
            y+=1
        else: 
            x+=1
            continue
        break
    return(isSame)

## FINGERPRINTS ## 
## FINGERPRINTS ## 
## FINGERPRINTS ## (COMMENT THE INTEGER PARTITIONING FUNCTION)


# COMMENT PROPERLY
# Generates a fingerprint given an arbitrary number of states and an arbitrary number of neighbours
# pls
def genFingerPrint(scoreMatrix):
    tempDic={}
    partitions=ascIntPart(numOfNeighbours)
    fingerPrint=fPrint()
    allParts=[]
    #Generates the integer partitions
    for partition in partitions:
        while len(partition) < numOfStates: # turns answers like 4 -> 4 0 0 0 (given we have four states)
            partition.append(0)
        if len(partition) == numOfStates:
            # Shift them over 4 0 0 0 -> 4 0 0 0, 0 4 0 0, 0 0 4 0, 0 0 0 4
            for n in range(numOfStates+1):
                allParts.append(partition)
                temp=copyList(partition)
                for x in range(len(partition)):
                    temp[x]=partition[(x+n)%len(partition)]
                    allParts.append(temp)
    #scores them
    for a in range(numOfStates):
        for partition in allParts:
            centerState=a
            score=0
            row=centerState*numOfStates
            # score fprint
            for state2,numOf in enumerate(partition):
                col = state2
                score+=numOf*scoreMatrix[row+col]
            tempDic[f"{centerState}:{partition}"]=score
    # This sorts the dictionary form lowest to highest, it uses a lambda function to make life easy
    # Note, we use the fingerprint data structure to make life easy
    fingerPrint.fPrint=sorted(tempDic.items(), key = lambda kv:(kv[1], kv[0]))
    fingerPrint.scoreMatrix=scoreMatrix
    return(fingerPrint)

# COMMENT PROPERLY
# Compares two fingerprints to see if theyre the same or not
# returns int, 1 is true 0 is false
def compareFPs(fPrint1,fPrint2):
    # Do the quick check (note default to -1)
    if ((fPrint1.behaviourNum > 0) and (fPrint2.behaviourNum > 0) and (fPrint1.behaivourNum == fPrint2.behaviourNum)):
        return(1)
    # If the quick check didnt work
    isSame = 1
    idx1 = 0
    idx2 = 0
    while (idx1 < len(fPrint1.fPrint)) and (isSame == 1):
        while (idx2 < len(fPrint2.fPrint)) and (isSame == 1):
            #checks if the strings are the same
            if (fPrint1.fPrint[idx1][0] != fPrint2.fPrint[idx2][0]):
                isSame = 0
            idx1+=1
            idx2+=1
        else: 
            continue
        break
    return(isSame)


    