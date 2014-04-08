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
# model constructor
class SimpleRumorModel():
  # k is built in to the spread chance and stifle chance because this model assumes
  # that every agent gets the chance to interact with each friend every day

  # TODO: we should change this... if 1% of interactions cause stifling, 
  # and someone with 500 friends interacts with all 500 every day, he has an 
  # unreasonably high chance of being stifled

  def __init__(self, graph, spreadChance=0.1, stifleChance=0.01, numSpreaders=5, contactFraction=0.1, spontaneousStifleChance=0.1,
    useContactFractionFunction=True):
    # parameters
    self.spreadChance = spreadChance
    self.stifleChance = stifleChance
    self.contactFraction = contactFraction
    self.spontaneousStifleChance = spontaneousStifleChance
    self.useContactFractionFunction = useContactFractionFunction
    self.t = 0

    self.graph = graph
    self.adjacencyMap = get_adjacency_map(graph)

    self.N = self.size(self.adjacencyMap)

    allAgents = get_node_ids(graph)

    #shuffle the list so there's no accidental correlation in agent actions
    # random.shuffle(allAgents) # I think this is useless...

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
      self.doSpontaneousStifle(spreader) # a spreader will spontaneously decide to be a stifler with some probability
    self.commitTempSets()

  def displayCounts(self):
    print "Time =",self.t
    print "Num ignorants:",self.numIgnorants()
    print "Num spreaders:",self.numSpreaders()
    print "Num stiflers:",self.numStiflers()
    print ""

  def numIgnorants(self):
    return self.size(self.ignorantSet)

  def numSpreaders(self):
    return self.size(self.spreaderSet)

  def numStiflers(self):
    return self.size(self.stiflerSet)

  # weird bug: lists and sets are overwritten by snap.py and don't have the len() function
  def size(self, iterable):
    count = 0
    for i in iterable:
      count+=1
    return count

  def getContactFraction(self):
    if not self.useContactFractionFunction: return self.contactFraction
    unit = self.contactFraction
    hour = self.t % 24 # 0 is noon
    fractions = {
    "0" : .5,
    "1" : .4,
    "2" : .3,
    "3" : .27,
    "4" : .27,
    "5" : .3,
    "6" : .4,
    "7" : .5,
    "8" : .8,
    "9" : 1.2,
    "10" : 1.6,
    "11" : 1.7,
    "12" : 1.7,
    "13" : 1.75,
    "14" : 1.77,
    "15" : 1.8,
    "16" : 1.7,
    "17" : 1.6,
    "18" : 1.5,
    "19" : 1.5,
    "20" : 1.4,
    "21" : 1.25,
    "22" : 1.0,
    "23" : 0.7
    }
    return unit * fractions[hour]

  def doSpontaneousStifle(self, spreader):
    if random.random() < self.spontaneousStifleChance:
      self.recover(spreader)

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
    for friend in self.getContactedFriends(spreader):
      if self.isIgnorant(friend):
        if random.random() < self.spreadChance:
          self.infect(friend)
          count += 1
    return count

  def getContactedFriends(self, node): # is a generator
    friends = self.adjacencyMap[node]
    random.shuffle(friends)
    num = int(self.contactFraction * self.size(friends))
    count = 0
    for friend in friends:
      if count == num: return
      yield friend

  def beStifled(self, spreader):
    for friend in self.getContactedFriends(spreader):
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



def defaults():
  return {
  "graph": 0,
  "spreadChance": 0.1,
  "stifleChance": 0.01,
  "numSpreaders": 5,
  "contactFraction" : 0.1,
  "spontaneousStifleChance" : 0.1,
  "useContactFractionFunction" : True
  }

def params_to_string(params):
  return "g: "+str(params["graph"]) + ", SpCh: "+ str(params["spreadChance"]) + \
  ", StCh: "+ str(params["stifleChance"]) + ", #Sp: "+ str(params['numSpreaders']) + \
  ", CF: "+ str(params["contactFraction"]) + ", SSC: "+ str(params["spontaneousStifleChance"]) + \
  ", UCFF: " + str(params['useContactFractionFunction'])

def check_default():
  args = sys.argv[1:]
  if args and args[0] == '-d':
    return True
  return False

def prompt_user():
  d = {}
  d['graph'] = int(raw_input("Enter Graph Number: ") or defaults()['graph'])
  d['spreadChance'] = float(raw_input("Enter Spread Chance: ") or defaults()['spreadChance'])
  d['stifleChance'] = float(raw_input("Enter Stifle Chance: ") or defaults()['stifleChance'])
  d['numSpreaders'] = int(raw_input("Enter Number of Spreaders: ") or defaults()['numSpreaders'])
  d['useContactFractionFunction'] = False if raw_input("Have K Vary by Time Of Day? (y/n): ") == 'n' else True
  d['contactFraction'] = float(raw_input("Enter Contact Fraction: ") or defaults()['contactFraction'])
  d['spontaneousStifleChance'] = float(raw_input("Enter Spontaneous Stifle Chance: ") or defaults()['spontaneousStifleChance'])
  return d


if __name__ == '__main__':
  params = defaults() if check_default() else  prompt_user()
  graph = loadGraph(params['graph'])
  # N = graph.GetNodes()
  #initial conditions (# of people in each state)
  model = SimpleRumorModel(graph, params['spreadChance'], params['stifleChance'], 
    params['numSpreaders'], params['contactFraction'], params['spontaneousStifleChance'],
    params['useContactFractionFunction'])
  #model.displayCounts()

  minIterations = 5
  maxIterations = 1000
  numSp = []
  numIg = []
  numSt = []
  time = []

  numSp.append(model.numSpreaders())
  numIg.append(model.numIgnorants())
  numSt.append(model.numStiflers())

  while model.t < minIterations or (model.numSpreaders() > 0 and model.t < maxIterations):
    model.run()
    #model.displayCounts()
    numSp.append(model.numSpreaders())
    numIg.append(model.numIgnorants())
    numSt.append(model.numStiflers())
    # pause = raw_input("hit any key to keep going... CTRL+C to quit")
  time = range(model.t)
  #print numSp
  #print numIg
  #print numSt

  title = "SIR - "+", ".join(list(str(key) + ": " + str(params[key]) for key in params))
  title = params_to_string(params)
  filename = "img/"+ re.sub('[^0-9a-zA-Z\.]+', '_', title)+".png"
  pl.subplot(211)
  pl.plot(numIg, '-g', label='Ignorants')
  pl.plot(numSt, '-k', label='Stiflers')
  pl.legend(loc=0)
  pl.title(title)
  pl.xlabel('Time')
  pl.ylabel('Ignorants and Stiflers')
  pl.subplot(212)
  pl.plot(numSp, '-r', label='Spreaders')
  pl.xlabel('Time')
  pl.ylabel('Spreaders')
  pl.savefig(filename)

