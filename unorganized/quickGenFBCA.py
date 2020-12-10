# This code (made as of Nov 2020) is meant to utilize 'crisscrossing' to generate complex level-maps.

# 

#imports of libraries
import libFBCAGen
import os 
import random
##INITS 
#defintions for FBCA generation
libFBCAGen.CALength=100 #Length of the generated image (for min use 5)
libFBCAGen.CAWidth=100 #Width of the generated image (for min use 4)
libFBCAGen.useImages=1 #generate gifs? 
libFBCAGen.finalImage=1 #generate final level map?
libFBCAGen.numOfGens=20 #number of generations
libFBCAGen.random.seed(1) #set to 1 for constant
d=[];d=os.getcwd()+"/" #Get directory
#Score matrices
sM1=[0.320205,0.952292,0.351335,0.837774]
sM2=[0.390741,0.728013,0.614486,0.378596]
sM3=[0.234,0.42,0.9271,0.59745]
sM4=[0.420,0.69,0.1337,0.8008]
sM5=[random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
sM6=[random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
sM7=[random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
sM8=[random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
sM9=[random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
sM10=[random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
sMs=[sM1,sM2,sM3,sM4,sM5,sM6,sM7,sM8,sM9,sM10]
#generate first guys
libFBCAGen.numOfStates=int(len(sM1)/2)
CAMapInit=[];CAMapInit=libFBCAGen.initCA(CAMapInit) #Get L_0
for idx,curSM in enumerate(sMs):    
    libFBCAGen.generateFBCA(curSM,d,CAMapInit,str(idx)) #Generate the final L_g
