# This code (made as of Dec 2020) is a method to generate linear morphs between a set of FBCA using fingerpritns
# 

#imports of libraries
import libFBCAGen
import os 
import numpy
from PIL import Image #for visualization through image generation

##DATA STRUCTURES BELOW ##
# This is dumb, it doesnt let me take the one from the library but AIGHT
class fPrint:
    fPrint=[]
    scoreMatrix=[]
    lambd=0
    xSpot=0
    behaviourNum=-1

##INITS 
## Morph visualziation varbs
morphRes=1000 #How many equally spaced score matrices are generated btwn sM1 and sM2
imageHeight=100 #Height of the generated image 
#Defintions for FBCA generation (this is used to generate the 'vertex CAs')
libFBCAGen.useImages=0 #generate gifs? 
libFBCAGen.finalImage=0 #generate final level map?
libFBCAGen.numOfGens=20 #number of generations
libFBCAGen.random.seed(1) #set to 1 for constant
libFBCAGen.numOfStates=4 #set correctly
CAMapInit=[];CAMapInit=libFBCAGen.initCA(CAMapInit) #Get L_0

d=[];d=os.getcwd()+"/" #Get directory
quantiferRead= "small"
quantifer = "small"

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


# Then lets generate their morphs
for n in range(0,len(sMs)-1): #Incase we have multiple matrices we want to morph between
    for m in range(n+1,len(sMs)):
        behaviours=[]
        fPs=[]
        quantifer = f"fMorph ({n},{m}) - {quantiferRead}"
        l=0
        for x in numpy.arange(0,1+1e-8,float(1/morphRes)): #In this loop we generate all the L_gs for the morph
            sMCur = libFBCAGen.genMorphSM(sMs[n],sMs[m],x) #gets score matrix for this point in the morph
            fPs.append(fPrint())
            fPs[len(fPs)-1].fP = libFBCAGen.genFingerPrint(sMCur) #gets the FP
            fPs[len(fPs)-1].lambd = x #Remembers the lambda used
            fPs[len(fPs)-1].xSpot = l #Remembers the column of pixels we are
            l+=1
        print(f"Done Generating fingerprint for ({n},{m})")
        # compares fingerprints
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
                temp.append(fpCur) #Add this one too
                ignoreList.append(idx) #ignore this one in the future
                behaviours.append(temp) #Add this behaviour class to the behaviours list

        print(f"Sorted FPs for ({n},{m})") #Makes it easier on the eyes
        morphRecord=open(f"fMorphPortrait record {quantifer}","w") # Records the behaviours
        morphRecord.write(f"All behaviours in morph of sMs{sMs[n]}sMs{sMs[n+1]} \n")
        for behaviour in behaviours:
            morphRecord.write(f"Behaviour similar to sM with lambda = {behaviour[0].lambd} \n")
        for behaviour in behaviours:
            if (libFBCAGen.useImages == 1):
                myEyes=str(round(behaviour[0].lambd,5))
                libFBCAGen.genIm(behaviour[0].fPrint,libFBCAGen.numOfGens,d,f"{quantifer} {myEyes}")
        #Generate the colours at the end?
        for n in range(0,len(sMs)-1): #Incase we have multiple matrices we want to morph between
            for m in range(n+1,len(sMs)):
                print(f"Generating Image for ({n},{m})")
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
                im.save(f"fMorph of {quantifer}.png")
                morphRecord.close()
                print(f"Done ({n},{m})")
