# Graph Morphs (maybe rename?)
# In short 
Graph morphs are a method to visualize all behaviours attained from a complete graph of linear morphs between multiple Fashion Based Cellular Automata. This is done through visualizing a 2D convex cross sections centered at every FBCA, represented by a m-sided polgyon, m being the number of members in the morphed set minus 1. This has shown to be a very easy method to describe similar score matrices for FBCA with an arbtirary number of states and, with small edits, should be able to visualize a 'pseudo phase portrait' for FBCAs an arbitrary number of states.  

# What
To start, one must be familiar with (FBCA; described in Section 1.1 , Linear morphs; described in Section 3.1, Behaviours; described in Section 2.1 and phase portraits described in Section 3.3 of https://atrium.lib.uoguelph.ca/xmlui/handle/10214/21316). These are also defined in the following papers (and are slightly more easy to read): . The following example of what a graph morph is can best be used to explain the work done.
Consider the following score matrices.


# Visualizing higher dimension FBCA space
Previous work with FBCAs revealed that FBCAs can be effectively sorted by their score matrices, provided all other paramters are held constant. Sorting by all possible score matrices is effective as all possible patterns (called behaviours due to patterns having some intrinsic property to them) produced by a FBCA can be recorded. The main issue with this method is the number of dimensions required to visualize the behaviours of FBCAs with more than two states. Since the dimension an FBCA's score matrices is the square of its number of states (_n_ > 1, in N) any method of visualziing all behaviours past the _n_ = 2 state case, (detailed in Section 3.3 here  https://atrium.lib.uoguelph.ca/xmlui/handle/10214/21316) is not easily done. To combat this a new method for visualizing this higher dimensional space is required. 

# Polyvision (name changeable)
While arbitrarily high dimensional dimensional space is difficult to visualize, any 2D convex cross section can be visualzied using a phase portrait. If 2D convex cross sections are smartly chosen, then all behaviours should be recordable. For now we shall ignore the problem of _smartly_ choosing behaviours and instead create a software to visualize these 2D convex cross sections. This is done through Polyvision and uses  
