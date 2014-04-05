import snap
from load import *

def draw(graph, filename, graphname):
  snap.DrawGViz(graph, snap.gvlDot, filename, graphname)

if __name == __main__:
  draw(loadGraph(0), "graph0.png", "graph 0")
