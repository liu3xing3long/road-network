import numpy as np
from matplotlib import pyplot as plt
import globals 

DEBUG = False

class QuadTree:

    # init
    def __init__(self, data, mins, maxs, depth, nodeId):

        if DEBUG: print "node id: "+str(nodeId)
        self.mins=mins
        self.maxs=maxs
        self.depth=depth
        self.n_nodeId=nodeId
        # update node Index
        globals.nodeIndex[nodeId]=depth
        self.data = np.asarray(data)

        assert self.data.shape[1] == 2

        if mins is None:
            mins = data.min(0)
        if maxs is None:
            maxs = data.max(0)

        self.mins = np.asarray(mins)
        self.maxs = np.asarray(maxs)
        self.sizes = self.maxs - self.mins

        self.children = []

    def add_square(self):

        mids = 0.5 * (self.maxs + self.mins)
        if DEBUG: print self.data
        if DEBUG: print mids
        xmin, ymin = self.mins
        xmax, ymax = self.maxs
        xmid, ymid = mids

        sq_q1 = self.data[(self.data[:, 0] < mids[0]) & (self.data[:, 1] < mids[1])]
        sq_q2 = self.data[(self.data[:, 0] < mids[0]) & (self.data[:, 1] >= mids[1])]
        sq_q3 = self.data[(self.data[:, 0] >= mids[0]) & (self.data[:, 1] < mids[1])]
        sq_q4 = self.data[(self.data[:, 0] >= mids[0]) & (self.data[:, 1] >= mids[1])]

        if DEBUG: print "d1:" + str(sq_q1)
        if DEBUG: print "d2:" + str(sq_q2)
        if DEBUG: print "d3:" + str(sq_q3)
        if DEBUG: print "d4:" + str(sq_q4)

        if DEBUG: print "depth: "+str(self.depth)

        nodeId=0
        if not globals.nodeIndex:
            nodeid=0
        else:
            nodeId=max(globals.nodeIndex)

        if DEBUG: print "* nodeid: "+str(nodeId)
        if sq_q1.shape[0] > 0:
            nodeId=nodeId+1
            self.children.append(QuadTree(sq_q1, [xmin, ymin], [xmid, ymid],self.depth + 1, nodeId))
                
        if sq_q2.shape[0] > 0:
            nodeId=nodeId+1
            self.children.append(QuadTree(sq_q2,[xmin, ymid], [xmid, ymax],self.depth + 1, nodeId))
                              
        if sq_q3.shape[0] > 0:
            nodeId=nodeId+1
            self.children.append(QuadTree(sq_q3,[xmid, ymin], [xmax, ymid],self.depth + 1, nodeId))
                                
        if sq_q4.shape[0] > 0:
            nodeId=nodeId+1
            self.children.append(QuadTree(sq_q4,[xmid, ymid], [xmax, ymax],self.depth + 1, nodeId))

    
    def __hash__(self):
        return hash(self.n_nodeId)

    def __eq__(self, other):
        return (self.n_nodeId) == (other.n_nodeId)                           

    def draw_rectangle(self, ax, depth):
        if depth is None or depth == 0:
            # print self.mins
            # print self.sizes
            rect = plt.Rectangle(self.mins, *self.sizes, zorder=2, ec='#000000', fc='none')
            ax.add_patch(rect)

        if depth is None or depth > 0:
            for child in self.children:
                child.draw_rectangle(ax, depth - 1)









