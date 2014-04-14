import matplotlib as mpl
mpl.use('Agg')
font = {'size' : 10}
mpl.rc('font', **font)

import random
import copy
import pylab as pl
#import scipy
#from scipy import random
#import heapq
from load import *
from lib import *
import sys
import re

def count(gid):
  graph = loadGraph(gid)
  print "graph: %d - size: %d  - avgN: %0.2f" %(gid,graph.GetNodes(), average_neighbors(graph))
if __name__ == "__main__":
  gids = [0,107,348,414,686,698,1684,1912,3437,3980]
  map(count, gids)

