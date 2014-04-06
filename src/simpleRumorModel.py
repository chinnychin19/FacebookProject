import random
import copy
import pylab as pl
import scipy
from scipy import random
import heapq
from load import *
from lib import *

# model constructor
class simpleRumorModel():
  # b - beta 
  # g - gamma
  #
  def __init__(self, b = .2, g=0.01, S=300, I=1, graph):
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

if __name__ == '__main__':
  #transmission parameters (daily rates scaled to hourly rates)
  b = .02 / 24.0
  g = .05 / 24.0

  graph = loadGraph(0)
  N = graph.GetNodes()
  #initial conditions (# of people in each state)
  S = N-3
  I = 3 
  
