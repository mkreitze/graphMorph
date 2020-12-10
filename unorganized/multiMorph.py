# This code (made as of Nov 2020) is meant to generate linear morphs between all members generated via a crisscross
# 

#imports of libraries
import libFBCAGen
import os 
import itertools
import numpy
from PIL import Image #for visualization through image generation

##DATA STRUCTURES BELOW ##
class lGContainer:
    lG=[]
    lambd=0
    xSpot=0

##INITS 
#defintions for FBCA generation
libFBCAGen.CALength=20 #Length of the generated image (for min use 5)
libFBCAGen.CAWidth=20 #Width of the generated image (for min use 4)
libFBCAGen.useImages=0 #generate gifs? 
libFBCAGen.finalImage=0 #generate final level map?
libFBCAGen.numOfGens=20 #number of generations
libFBCAGen.random.seed(1) #set to 1 for constant
libFBCAGen.numOfStates=2 #set correctly
d=[];d=os.getcwd()+"/" #Get directory
quantiferRead= "test"
quantifer = "test"
CAMapInit=[];CAMapInit=libFBCAGen.initCA(CAMapInit) #Get L_0

#Score matrix inits
crissCrossRecord=open(f"crissCross {quantifer}", "r")
sMs=[]
for line in crissCrossRecord:
    line=line.split(":")[2][:-2]
    sMs.append(libFBCAGen.convTextListToList(line))
##Important varbs
morphRes=1000 #How many equally spaced score matrices are generated btwn sM1 and sM2
imageHeight=100 #Height of the generated image 

# This is inefficient please fix in the future
libFBCAGen.finalImage=1 #generate final level map?
libFBCAGen.useImages=1 #generate gifs? 
for n in range(0,len(sMs)): #Incase we have multiple matrices we want to morph between
    libFBCAGen.generateFBCA(sMs[n],d,CAMapInit,str(n)) #Generate the final L_g
libFBCAGen.finalImage=0 #generate final level map?
libFBCAGen.useImages=0 #generate gifs? 


## MAIN ##
for n in range(0,len(sMs)-1): #Incase we have multiple matrices we want to morph between
    for m in range(n+1,len(sMs)):
        lGs=[]
        behaviours=[]
        quantifer = f"morph ({n},{m}) - {quantiferRead}"
        l=0
        for x in numpy.arange(0,1+1e-8,float(1/morphRes)): #In this loop we generate all the L_gs for the morph
            sMCur = libFBCAGen.genMorphSM(sMs[n],sMs[m],x) #gets score matrix
            lGs.append(lGContainer())
            lGs[len(lGs)-1].lG = libFBCAGen.generateFBCA(sMCur,d,CAMapInit,x) #gets the L_g
            lGs[len(lGs)-1].lambd = x #Remembers the lambda used
            lGs[len(lGs)-1].xSpot = l #Remembers the column of pixels we are
            l+=1
        print(f"Done Generating Lambdas for ({n},{m}) - {quantifer}")
        ignoreList=[]
        for idx,lgCur in enumerate(lGs): #Sorts each L_g into behaviour groups
            temp=[] #This will hold all the similar L_gs
            ignore=0
            for val in ignoreList: #Makes sure I shouldnt ignore it 
                if val == idx:
                    ignore=1
            if ignore == 0:
                for idx2,lgNew in enumerate(lGs): #Walk through the rest
                    if (libFBCAGen.compareLs(lgCur,lgNew) == 1): #If similar, add to the list
                        temp.append(lgNew)
                        ignoreList.append(idx2) #Remove the similar one
                temp.append(lgCur)
                ignoreList.append(idx) 
                behaviours.append(temp) #Add this behaviour class to the behaviours list
        print(f"Sorted L_gs for ({n},{m})") #Makes it easier on the eyes
        morphRecord=open(f"morphPortrait record {quantifer}","w")
        morphRecord.write(f"All behaviours in morph of sMs{sMs[n]}sMs{sMs[n+1]} \n")
        for behaviour in behaviours:
            morphRecord.write(f"Behaviour similar to sM with lambda = {behaviour[0].lambd} \n")
        for behaviour in behaviours:
            if (libFBCAGen.useImages == 1):
                myEyes=str(round(behaviour[0].lambd,5))
                libFBCAGen.genIm(behaviour[0].lG,libFBCAGen.numOfGens,d,f"{quantifer} {myEyes}")
        print(f"Generating Image for ({n},{m}) - {quantifer}")
        #Probably should comment this below
        imageColourStep=(255*3)/(len(behaviours))
        im= Image.new('RGB', ((morphRes+1),imageHeight), 1)
        for idx,behaviour in enumerate(behaviours):
            colourVal=int(idx*imageColourStep)
            if (colourVal-255<0):
                r = colourVal
                g=0
                b=0
            else:
                r=255
                colourVal-=255
                if (colourVal-255<0):
                    g = colourVal
                    b=0
                else:
                    g=255
                    colourVal-=255
                    if (colourVal-255<0):
                        b = colourVal
                    else:
                        b=255
            for thing in behaviour:
                for y in range(0,(imageHeight)):
                    im.putpixel((thing.xSpot,y),(r,g,b))
        im.save(f"morph of {quantifer}.png")
        morphRecord.close()
        print(f"Done ({n},{m})")
