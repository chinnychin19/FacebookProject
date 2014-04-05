from snap import *
from load import *

def main():
  G = loadGraph(0)
  for EI in G.Edges():
    print "edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())

if __name__ == '__main__':
  main()
