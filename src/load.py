from snap import *

G = TUNGraph.New()

def loadGraph(root):
  filename = "../data/%d.edges"%root
  G.AddNode(root)
  lines = open(filename).read().split('\n')[0:-1]
  for line in lines:
    nums = line.split(' ')
    nodeA = int(nums[0])
    nodeB = int(nums[1])

    if not G.IsNode(nodeA):
      G.AddNode(nodeA)
    if not G.IsNode(nodeB):
      G.AddNode(nodeB)

    G.AddEdge(nodeA, nodeB)

    if not G.IsEdge(root, nodeA):
      G.AddEdge(root, nodeA)
    if not G.IsEdge(root, nodeB):
      G.AddEdge(root, nodeB)


  return G
if __name__ == '__main__':
  loadGraph(0)
