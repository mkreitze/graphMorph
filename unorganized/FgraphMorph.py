# This code (made as of Dec 2020) is a method to generate linear morphs between a set of FBCA using fingerpritns
# 

#imports of libraries
import libFBCAGen
import os 
import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
import math
from PIL import Image #for visualization through image generation

##DATA STRUCTURES BELOW ##
# This is dumb, it doesnt let me take the one from the library but AIGHT
class fPrint:
    fPrint=[]
    scoreMatrix=[]
    lambd=0
    xSpot=0
    behaviourNum=-1
    morphNum=[]

##INITS 
## Morph visualziation varbs
morphRes=100 #How many equally spaced score matrices are generated btwn sM1 and sM2
imageHeight=100 #Height of the generated image 
genPolyGraph = 1 # 0 is false
polyGraphRadius = 10; 
#Defintions for FBCA generation (this is used to generate the 'vertex CAs')
libFBCAGen.useImages=0 #generate gifs? 
libFBCAGen.finalImage=0 #generate final level map?
libFBCAGen.numOfGens=20 #number of generations
libFBCAGen.random.seed(1) #set to 1 for constant
libFBCAGen.numOfStates=2 #set correctly
CAMapInit=[];CAMapInit=libFBCAGen.initCA(CAMapInit) #Get L_0

d=[];d=os.getcwd()+"/" #Get directory
quantiferRead= "2smaller"
quantifer = "2smaller"

#Score matrix inits
crissCrossRecord=open(f"crissCross {quantifer}", "r")
sMs=[]
for line in crissCrossRecord:
    line=line.split(":")[2][:-2]
    sMs.append(libFBCAGen.convTextListToList(line))

## MAIN ## 

# Generates the images for the vertexs 
libFBCAGen.finalImage=1 #generate final level map?
libFBCAGen.useImages=1 #generate gifs? 
for n in range(0,len(sMs)):
    libFBCAGen.generateFBCA(sMs[n],d,CAMapInit,str(n)) #Generate the final L_g
libFBCAGen.finalImage=0 #generate final level map?
libFBCAGen.useImages=0 #generate gifs? 

# Figures out how many finger prints per morph

# Then lets generate their morphs and resulting fingerprints
fPs=[]
for n in range(0,len(sMs)-1): #Incase we have multiple matrices we want to morph between
    for m in range(n+1,len(sMs)):
        quantifer = f"fMorph ({n},{m}) - {quantiferRead}"
        l=0
        for x in numpy.arange(0,1+1e-8,float(1/morphRes)): #In this loop we generate all the L_gs for the morph
            sMCur = libFBCAGen.genMorphSM(sMs[n],sMs[m],x) #gets score matrix for this point in the morph
            fPs.append(fPrint())
            fPs[len(fPs)-1].fP = libFBCAGen.genFingerPrint(sMCur) #gets the FP
            fPs[len(fPs)-1].scoreMatrix=sMCur
            fPs[len(fPs)-1].lambd = x #Remembers the lambda used
            fPs[len(fPs)-1].xSpot = l #Remembers the column of pixels we are
            fPs[len(fPs)-1].morphNum = (n,m) #Remembers which morph this is
            l+=1
        print(f"FPed morph ({n},{m})")
# Now lets sort the fingerprints into iso-behavioural grains
behaviours=[]
ignoreList=[]
for idx,fpCur in enumerate(fPs): #Sorts each L_g into behaviour groups
    temp=[] #This will hold all the similar L_gs
    ignore=0 
    for val in ignoreList: #Makes sure I shouldnt ignore it 
        if val == idx:
            ignore=1            
    if ignore == 0: #If were NOT supposed to ignore it 
        for idx2,fpNew in enumerate(fPs): #Walk through the rest 
            if (libFBCAGen.compareFPs(fpCur.fP,fpNew.fP) == 1): #If similar, add to the list
                temp.append(fpNew)
                ignoreList.append(idx2) #In the future, ignore the similar one
                fpNew.behaviourNum=len(behaviours)
        temp.append(fpCur) #Add this one too
        ignoreList.append(idx) #ignore this one in the future
        behaviours.append(temp) #Add this behaviour class to the behaviours list
        fpCur.behaviourNum=len(behaviours)
print(f"Sorted FPs") #Makes it easier on the eyes

# Now lets generate the images 
l = 0
print(f"Generating Image for ({fPs[0].morphNum[0]},{fPs[0].morphNum[1]})")
im= Image.new('RGB', ((morphRes+1),imageHeight), 1)
for fpCur in fPs: # walk through the fingerprints
    if l >= morphRes: 
    #Probably should comment this below
        im.save(f"fGraph of ({fpCur.morphNum[0]},{fpCur.morphNum[1]}).png")
        print(f"Generating Image for ({fpCur.morphNum[0]},{fpCur.morphNum[1]})")
        im= Image.new('RGB', ((morphRes+1),imageHeight), 1)
        l=0
    rgb=libFBCAGen.getBehCol(fpCur.behaviourNum,behaviours)

    for y in range(0,(imageHeight)):
        im.putpixel((l,y),rgb)
    l+=1


# Incase the colouring the polygraph method might be useful
# double check this 
point1 = [polyGraphRadius,0]
magma = cm.get_cmap('gist_ncar', len(behaviours)) 
for n in range(0,len(sMs)-1): # go through each
    xs=[];ys=[];theta=0 #stuff for plotting
    fig = plt.figure()
    ax1=plt.axes()
    for vTex in range(len(sMs)-1): #get xs and ys for the polygons we make (below code makes the polygons)
        if vTex==0:
            xs.append(point1[0])
            ys.append(point1[1])
        else:
            theta=2*vTex*math.pi/(len(sMs)-1)
            xs.append(polyGraphRadius*math.cos(theta))
            ys.append(polyGraphRadius*math.sin(theta))
    ax1.set_xlim(-polyGraphRadius-1,polyGraphRadius+1)
    #change to y if custom
    ax1.set_ylim(-polyGraphRadius-1,polyGraphRadius+1)
    ax1.scatter(xs,ys)
    for idx,behaviour in enumerate(behaviours):
        for m in range(len(sMs)-1): # skip the same number
            newXs=[];newYs=[]
            for fingy in behaviour:
                if (fingy.morphNum[1] == m) or (fingy.morphNum[0] == m):
                    if (fingy.morphNum[1] == n) or (fingy.morphNum[0] == n):
                        newXs.append(fingy.xSpot*xs[m]/morphRes)
                        newYs.append(fingy.xSpot*ys[m]/morphRes)
            ax1.scatter(newXs,newYs,c=magma(idx))
    plt.savefig(str(n)+".png")
# Save found behaviours in a folder
libFBCAGen.makeFolder(behaviours)

# Generates the images for the vertexs 
libFBCAGen.finalImage=1 #generate final level map?
libFBCAGen.useImages=1 #generate gifs? 
for idx,behaviour in enumerate(behaviours):
    libFBCAGen.generateFBCA(behaviour[0].scoreMatrix,f"{d}behaviours/",CAMapInit,str(idx)) #Generate the final L_g
libFBCAGen.finalImage=0 #generate final level map?
libFBCAGen.useImages=0 #generate gifs? 
