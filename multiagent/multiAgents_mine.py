# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        #print successorGameState
        newPos = successorGameState.getPacmanPosition()
        #print newPos
        newFood = successorGameState.getFood()
        #print newFood
        newGhostStates = successorGameState.getGhostStates()
        #print newGhostStates
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print newScaredTimes
        "*** YOUR CODE HERE ***"
        distance = []                                                                           #create a list to track the manhattan distance between food and pacman
        foodlist = currentGameState.getFood().asList()                                          #maintain the list of food positions in the state. Each dot represents food and is displayed as T/F
        #print foodlist
        pacmanPos = list(newPos)                                                                #returns the list of Pacman position
        #print pacmanPos
        ghostPos = ghostState.getPosition()
        #print ghostPos

        #this returns a very high negative value if the below conditions are true
        
        if action == 'Stop':                                        
            return -float("inf")

        for ghostState in newGhostStates:
            if ghostPos == tuple(pacmanPos) and ghostState.scaredTimer is 0:    #if ghost and pacman collide i.e. they have same positions and there is no timer running
                return -float("inf")
            
        
        for food in foodlist:
            man_dist = abs(food[0] - pacmanPos[0])+abs(food[1] - pacmanPos[1])                  #calculate the manhattan distance between the food and pacman
            inverse_man_dist = -man_dist                                                     #take the negative of the manhattan distance
            distance.append(inverse_man_dist)                                                #append the distances in the list maintained

        return max(distance)                                                                    #return maximum of the distances
        
        #return successorGameState.getScore()
        
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        depth = 0
        
        agentIndex = 0

        value = self.func(gameState, agentIndex, depth)
        return value[0]
    
    def func(self, gameState, agentIndex, depth):

        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth = depth +1
            
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        
        if agentIndex == 0:
            max_val = self.max_func(gameState, agentIndex, depth)
            return max_val
        else:
            min_val = self.min_func(gameState, agentIndex, depth)
            return min_val

    "This function will return the minimum value of the nodes at current depth 'depth'"
    def min_func(self, gameState, agentIndex, depth):

        v = ("test",float("inf"))

        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        
        for action in gameState.getLegalActions(agentIndex):
            if action == "Stop":
                continue

            succ = gameState.generateSuccessor(agentIndex,action)
            value = self.func(succ, agentIndex+1, depth)

            if type(value) is tuple:
                #print value
                value = value[1]

            minimum = min(v[1],value)

            if minimum is not v[1]:
                v = (action, minimum)
                        
        return v
        
    "This function will return the maximum value of the nodes at current depth 'depth'"
    def max_func(self, gameState, agentIndex, depth):

        v = ("test",-float("inf"))

        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        
        for action in gameState.getLegalActions(agentIndex):
            if action == "Stop":
                continue

            succ = gameState.generateSuccessor(agentIndex,action)
            value = self.func(succ, agentIndex+1, depth)

            if type(value) is tuple:
                #print value
                value = value[1]

            maximum = max(v[1],value)
                
            if maximum is not v[1]:
                v = (action, maximum)
                        
        return v

        
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          #Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        util.raiseNotDefined()
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        depth = 0
        
        agentIndex = 0

        value = self.func(gameState, agentIndex, depth)
        return value[0]
    
    def func(self, gameState, agentIndex, depth):

        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth = depth +1
            
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        
        if agentIndex == 0:
            max_val = self.max_func(gameState, agentIndex, depth)
            return max_val
        else:
            exp_val = self.exp_func(gameState, agentIndex, depth)
            return exp_val
        
    "This function will return the expected value of the nodes at current depth 'depth'"
    def exp_func(self, gameState, agentIndex, depth):

        v = ["test", 0]

        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

        prob = 1.0/len(gameState.getLegalActions(agentIndex))           #determines the probabilistic behaviour of agents
        
        for action in gameState.getLegalActions(agentIndex):
            if action == "Stop":
                continue

            succ = gameState.generateSuccessor(agentIndex,action)
            value = self.func(succ, agentIndex+1, depth)

            if type(value) is tuple:
                #print value
                value = value[1]

            v[1] += value * prob
            v[0] = action
                        
        return tuple(v)
        
    "This function will return the maximum value of the nodes at current depth 'depth'"
    def max_func(self, gameState, agentIndex, depth):

        v = ("test",-float("inf"))

        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        
        for action in gameState.getLegalActions(agentIndex):
            if action == "Stop":
                continue

            succ = gameState.generateSuccessor(agentIndex,action)
            value = self.func(succ, agentIndex+1, depth)

            if type(value) is tuple:
                #print value
                value = value[1]

            maximum = max(v[1],value)
                
            if maximum is not v[1]:
                v = (action, maximum)
                        
        return v
        
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

