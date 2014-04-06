import random
import copy
#import pylab as pl
#import scipy
#from scipy import random
#import heapq
from load import *
from lib import *

# model constructor
class simpleRumorModel():
  # b - beta 
  # g - gamma
  #
  def __init__(self, b = .2, g=0.01, S=1, I=300, graph):
    # parameters
    self.b = b
    self.g = g
    self.t = 0
    self.p = p

    self.N = S+I
    self.graph = graph
    self.adjacencyMap = get_adjacency_map(graph)

    #going to use this to store the *indices* of agents in each state
    self.sAgentList = []
    self.iAgentList = []
    self.rAgentList = []
    #here we're going to store the counts of how many agents are in each
    #state @ each time step
    self.sList = []
    self.iList = []
    self.rList = []

    allAgents = get_node_ids(graph)

    #shuffle the list so there's no accidental correlation in agent actions
    random.shuffle(allAgents)

    self.sAgentList = allAgents[0:S]
    self.iAgentList = allAgents[S:-1]

  def run():

if __name__ == '__main__':
  #transmission parameters (daily rates scaled to hourly rates)
  b = .02 / 24.0
  g = .05 / 24.0

  graph = loadGraph(0)
  N = graph.GetNodes()
  #initial conditions (# of people in each state)
  I = N-3
  S = 3 
  
