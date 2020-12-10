# test 
import libFBCAGen
libFBCAGen.CALength=20 #Length of the generated image (for min use 5)
libFBCAGen.CAWidth=20 #Width of the generated image (for min use 4)
libFBCAGen.useImages=0 #generate gifs? 
libFBCAGen.finalImage=0 #generate final level map?
libFBCAGen.numOfGens=20 #number of generations
libFBCAGen.random.seed(1) #set to 1 for constant
libFBCAGen.numOfStates=2 #set correctly

sM = [0.390741, 0.728013, 0.614486, 0.378596, 0.320205, 0.952292, 0.351335, 0.837774, 0.390741, 0.728013, 0.614486, 0.378596, 0.320205, 0.952292, 0.351335, 0.837774]

fPrintIs=libFBCAGen.genFingerPrint(sM)
for a in fPrintIs.fPrint:
    print(a)
