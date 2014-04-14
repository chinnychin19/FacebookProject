import snap
from load import *

def get_friends(G, nodeId):
  NodeVec = snap.TIntV()
  snap.GetNodesAtHop(G, nodeId, 1, NodeVec, False)
  return NodeVec

def get_adjacency_map(G):
  adjacency_map = {}
  for node in G.Nodes():
    adjacency_map[node.GetId()] = get_friends(G, node.GetId())
  return adjacency_map

def average_neighbors(G):
  adj = get_adjacency_map(G)
  total = sum(size(adj[key]) for key in adj)
  return total/float(size(adj.keys()))

def get_node_ids(G):
  return map(nodeId, G.Nodes())


def nodeId(node):
  return node.GetId()
if __name__ == '__main__':
  g = loadGraph(0)
  friends = get_friends(g, 24)
  for node in friends:
    print node
  print "total: %d" % len(friends)

  adj_map = get_adjacency_map(g)
  print len(adj_map[24])

def size( iterable):
  count = 0
  for i in iterable:
    count+=1
  return count

