# Graph Morphs (maybe rename?)
# In short 
Graph morphs are a method to visualize all behaviours attained from a complete graph of linear morphs between multiple Fashion Based Cellular Automata. This is done through visualizing a planar graph with verticies being each FBCA in the set and the edges being these linear morphs between each. This has shown to be a very easy method to describe similar score matrices for FBCA with an arbtirary number of states and, with small edits, should be able to visualize a 'pseudo phase portrait' for FBCAs an arbitrary number of states.  

To use any of this software download the folder 'code'.
The following libraries are needed to run this: os, numpy, matplotlib, math and PIL to run this software.
To generate all linear morphs between an inputted set use FmultiMorph.py. This code is run using the command 'python3 FmultiMorph.py'
To generate planar views of linear morphs for a set (and also record all unique behaviours found by the graph morph) use FgraphMorph.py.
This code is run using the command 'python3  FgraphMorph.py'

# Introduction
To start, one must be familiar with (FBCA; described in Section 1.1 , Linear morphs; described in Section 3.1, Behaviours; described in Section 2.1 and Phase Portraits described in Section 3.3 of https://atrium.lib.uoguelph.ca/xmlui/handle/10214/21316). These are also defined in the following papers (and are slightly more easy to read): . To better understand what the problem of visualizing the behaviours of FBCAs condsider the following example.

# A simple example

Consider the following two FBCAs with 2 states which both produce a behaviour that is organized enough to be used in level map generation:
sM1:[0.320205, 0.952292, 0.351335, 0.837774] : 

![sM1](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/test/0/0%2020.png)

sM2:[[0.390741, 0.728013, 0.614486, 0.378596]

![sM2](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/test/1/1%2020.png)

To add more complexity and better understand where similar matrices may be found in FBCAs with more states, a method known as crisscrossing (detailed here: https://github.com/mkreitze/crissCross {name change?}) was used. This method takes the two score matrices sM1 and sM2 and used them as the rows for the higher state FBCAs. These are denoted by the order each row (top down) is used. For example, sM(1,1,1,1) has the first score matrix used every time, as the rows of the four state score matrix. The number of options produced by this crisscrossing is the same as the number of possibilities generated by a two character alphabet on a four member string. All 2^4 = 16 options are recorded below. 

_ sM(2,2,2,2) ___ sM(2,2,2,1): ___ sM(2,2,1,1): ___ sM(2,1,1,1):  __ sM(1,1,1,1): ___ sM(1,1,1,2): __ sM(1,1,2,1): ___ sM(1,2,1,1): __ sM(2,1,1,2): ___ 

![sM2222](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/0/0%2020.png) ![sM2221](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/1/1%2020.png) ![sM2211](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/2/2%2020.png) ![sM2111](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/3/3%2020.png) ![sM1111](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/4/4%2020.png) ![sM1112](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/5/5%2020.png) ![sM1121](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/6/6%2020.png) ![sM1211](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/7/7%2020.png) ![sM2112](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/8/8%2020.png) 


_ sM(1,1,2,2): ___ sM(1,2,2,1): ___ sM(2,2,1,2): ___ sM(2,1,2,1): __ sM(1,2,1,2): ___ sM(2,1,2,2): __ sM(1,2,2,2): ___

![sM1122](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/9/9%2020.png) ![sM1221](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/10/10%2020.png) ![sM2212](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/11/11%2020.png) ![sM2112](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/12/12%2020.png) ![sM1212](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/13/13%2020.png) ![sM2122](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/14/14%2020.png) ![sM1222](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/fullExample/15/15%2020.png)

While 16 generated score matrices is useful. The number of linear morphs generated is 136, considerably higher than 16. This comes from the completed graph having the number of edges equal to the sum from 0 to i of n, with i being the number of members. 

To better visualize each of the 136 linear morphs, 16 planar graphs are generated. Due to current complications the first 8 score matrices and their associated planar graphs are generated below. 
##Each vertex should be named to make the planar graphs easier to visualize. ##

# <div align="center"> sM(2,2,2,2) 

![sM2222PG](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/firstNine/0.png)

# <div align="center"> sM(2,2,2,1): 

![sM2221PG](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/firstNine/1.png) 

# <div align="center"> sM(2,2,1,1): 

![sM2211PG](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/firstNine/2.png)

# <div align="center"> sM(2,1,1,1): 

![sM2111PG](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/firstNine/3.png)

# <div align="center"> sM(1,1,1,1): 

![sM1111PG](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/firstNine/4.png)

# <div align="center"> sM(1,1,1,2): 

![sM1112PG](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/firstNine/5.png)

# <div align="center"> sM(1,1,2,1): 

![sM1121PG](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/firstNine/6.png)

# <div align="center"> sM(1,2,1,1): 

![sM1211PG](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/firstNine/7.png) 


The main issue from using this method from crissCrosses is two fold. First, the visualization is not very useful as the colours give somewhat inconclusive results. This comes from the absurd number of behaviours detected by a crisscross. Infact, when trying to process all 16 points, the computation exits before completion due to computational strain. This leads to a huge number of colours being required to properly (889 different behaviours). Note, the maximal number of behaviours is actually pretty easy to calculate and will quickly be explained here. 

# An upper bound on behaviours
Consider an FBCA with n states, whose cells are all connected to m neighbours. As shown in previous work (https://atrium.lib.uoguelph.ca/xmlui/handle/10214/21316), an FBCA will have a different behaviour when the ordered set of inequalities represented by its score matrix rearranges. Therefore the number of behaviours that can exist, is the number of unique arrangements. 

To figure out the number of unique arrangements one must first tabulate the size of the set that must be arranged. Since every cell has m neighbours and each neighbour can have any state 1 to n, but the order of these states does not matter (1,1,1,2 == 2,1,1,1) this problem can be reframed as a 'identical balls in bins' problem. The balls in this case are each neighbour (therefore there are m balls) and the bins are the number of states (therefore there are n bins). Using the generic formula yields (n + m - 1) choose (m) to find cardinality of the rearrangeable set (Note this does NOT give us what those are but using integer partitions does). Now that we have the number of objects that can be arranged, consider that they are arranged with no ties. That is, the set possible score is a totally ordered. We can vary this by.... . Incorporating ties we include ... Therefore we have an upperbound on the number of behaviours in an FBCA with n states and whose cells each have m members. 

# A good sampling set

Given the abusrd number of behaviours seen by the crisscrossing method, this method of generating planar graphs and recording the behaviours should be able to effectively sample most behaviours found in high state FBCA. The reason for this is not known.

# Dectecting 'behaviourally close' FBCA

To better express the power of classifying 'behavioural distance' consider the following 2 state FBCA. The exact values used in the score matrices are detailed inthe 2dim example textfile.

![1](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/0/0%2020.png) ![2](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/1/1%2020.png) ![3](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/2/2%2020.png) ![4](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/3/3%2020.png) ![5](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/4/4%2020.png)![6](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/5/5%2020.png) ![7](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/6/6%2020.png) ![8](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/7/7%2020.png)

Their resulting planar graphs are (in order):

![1](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/0.png)

![2](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/1.png) 

![3](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/2.png)

![4](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/3.png)

![5](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/4.png)

![6](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/5.png)

![7](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/6.png)

![8](https://github.com/mkreitze/graphMorph/blob/master/multipleMorphs/fingerprintMethod/graphMorph/2dim/7.png) 
