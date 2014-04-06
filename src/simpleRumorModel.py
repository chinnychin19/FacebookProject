import random
import copy
#import pylab as pl
#import scipy
#from scipy import random
#import heapq
from load import *
from lib import *

# model constructor
class SimpleRumorModel():
  # k is built in to the spread chance and stifle chance because this model assumes
  # that every agent gets the chance to interact with each friend every day

  # TODO: we should change this... if 1% of interactions cause stifling, 
  # and someone with 500 friends interacts with all 500 every day, he has an 
  # unreasonably high chance of being stifled

  def __init__(self, graph, spreadChance=0.1, stifleChance=0.005, numSpreaders=5):
    # parameters
    self.spreadChance = spreadChance
    self.stifleChance = stifleChance
    self.t = 0

    self.graph = graph
    self.adjacencyMap = get_adjacency_map(graph)

    self.N = self.size(self.adjacencyMap)

    allAgents = get_node_ids(graph)

    #shuffle the list so there's no accidental correlation in agent actions
    random.shuffle(allAgents) # TODO: I think this is useless...

    self.spreaderSet = set(allAgents[0:numSpreaders])
    self.ignorantSet = set(allAgents[numSpreaders:-1])
    self.stiflerSet  = set()

  def run(self):
    self.t += 1
    self.tempSpreaderSet = set()
    self.tempStiflerSet = set()
    for spreader in self.spreaderSet:
      self.doSpread(spreader)  # a spreader does spread to ignorants
      self.beStifled(spreader) # a spreader is stifled by stiflers and other spreaders
    self.commitTempSets()

  def displayCounts(self):
    print "Time =",self.t
    print "Num ignorants:",self.size(self.ignorantSet)
    print "Num spreaders:",self.size(self.spreaderSet)
    print "Num stiflers:",self.size(self.stiflerSet)
    print ""

  # weird bug: lists and sets are overwritten by snap.py and don't have the len() function
  def size(self, iterable):
    count = 0
    for i in iterable:
      count+=1
    return count

  # takes all temp changes and commits them to permanent sets
  def commitTempSets(self):
    for node in self.tempSpreaderSet:
      self.spreaderSet.add(node)
      self.ignorantSet.remove(node)
    for node in self.tempStiflerSet:
      self.stiflerSet.add(node)
      self.spreaderSet.remove(node)

  def doSpread(self, spreader): # returns number of friends infected by this call
    count = 0
    for friend in self.adjacencyMap[spreader]:
      if self.isIgnorant(friend):
        if random.random() < self.spreadChance:
          self.infect(friend)
          count += 1
    return count

  def beStifled(self, spreader):
    for friend in self.adjacencyMap[spreader]:
      if self.isSpreader(friend) or self.isStifler:
        if random.random() < self.stifleChance:
          self.recover(spreader) # spreader becomes a stifler
          return True
    return False

  def infect(self, node):
    self.tempSpreaderSet.add(node)

  def recover(self, node):
    self.tempStiflerSet.add(node)

  def isIgnorant(self, node):
    return node in self.ignorantSet

  def isSpreader(self, node):
    return node in self.spreaderSet

  def isStifler(self, node):
    return node in self.stiflerSet




if __name__ == '__main__':
  graph = loadGraph(0)
  # N = graph.GetNodes()
  #initial conditions (# of people in each state)
  model = SimpleRumorModel(graph)

  while True:
    model.run()
    model.displayCounts()
    pause = raw_input("hit any key to keep going... CTRL+C to quit")
