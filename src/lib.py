import snap
from load import *

def get_friends(G, nodeId):
  NodeVec = snap.TIntV()
  snap.GetNodesAtHop(G, nodeId, 1, NodeVec, False)
  return NodeVec

if __name__ == '__main__':
  g = loadGraph(0)
  friends = get_friends(g, 24)
  for node in friends:
    print node
  print "total: %d" % len(friends)

