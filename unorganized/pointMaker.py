# This code (made as of Dec 2020) just generates polygons with n vertices that form lines going to the center
# 

#imports of libraries
import libFBCAGen
import os 
import numpy
import math
import matplotlib.pyplot as plt


numOfSides=2
r=2.0
point1=[r,0]
bigNum=20
allPoints=10
while numOfSides<bigNum:
    xs=[]
    ys=[]
    theta=0
    for vTex in range(numOfSides): #get xs and ys for the polygons we make   
        if vTex==0:
            xs.append(point1[0])
            ys.append(point1[1])
        else:
            theta=2*vTex*math.pi/numOfSides
            xs.append(r*math.cos(theta))
            ys.append(r*math.sin(theta))
        lastX=xs[len(xs)-1];lastY=ys[len(ys)-1]
        for point in range(1,allPoints):
            xs.append(point*lastX/allPoints)
            ys.append(point*lastY/allPoints)


    #Generate plot
    fig = plt.figure()
    ax1=plt.axes()
    ax1.set_xlim(-r-1,r+1)
    #change to y if custom
    ax1.set_ylim(-r-1,r+1)
    #generate line
            
    ax1.scatter(xs,ys)
    #save the image
    plt.savefig(str(numOfSides)+".png")
    numOfSides+=1
