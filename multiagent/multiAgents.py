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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
     
        "*** YOUR CODE HERE ***"
        
        
        
        newScore=successorGameState.getScore()
        ghostDistances = []
        foodDistances=[]
        foodPositions = currentGameState.getFood().asList()

        
        # calculates manhattan distance between ghost positions and pacman, and subtracts the reciprocal of maximum distance to score
        
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()            
            ghostDistances.append(util.manhattanDistance(newPos, ghostPos))         
        if min(ghostDistances) != 0 and ghostDistances:
            newScore-= 1.0/min(ghostDistances)
        else:
            return float('-inf')
        
        # calculates manhattan distance between food positions and pacman, and adds the reciprocal of minimum distance to score
        
        for foodPos in foodPositions:
            foodDistances.append(util.manhattanDistance(newPos, foodPos))       
        if min(foodDistances) != 0 and foodDistances:
            newScore+= 1.0/min(foodDistances)
        else:
            return float('inf')         
            

        return newScore     
        
        
"""
        
def manhattanDistance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
"""
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
      
    #s = 0
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
        self.s = 0
        def minValue(state, depth, agentIndex):
            
            # reassigns agentIndex to 0 if all the players has played and next is pacman's move
            if agentIndex == state.getNumAgents():
                return maxValue(state, depth - 1)

            # initializes val to +infinity
            val = float('inf')
            prevVal=val
            
            # gets legalActions for the agentIndex
            legalMoves=[]            
            legalMoves = state.getLegalActions(agentIndex)
            
            for action in legalMoves:
                # finds min value for the agent and assigns it to val
                val= min(val,minValue(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
                self.s +=1
               
            # terminates if value of val has not been changed i.e. there are more legalMoves left    
            if prevVal== val:
                return self.evaluationFunction(state)

            
            return val

        def maxValue(state, depth):
            
            #terminates if we have reached the bottom
            if depth ==0 :
                return self.evaluationFunction(state)
            
            # initializes val to -infinity
            val = float('-inf')
            prevVal=val
            
            # gets legalActions for pacman
            legalMoves=[]                     
            legalMoves = state.getLegalActions()
            
            for action in legalMoves:
                # finds max value for pacman and assigns it to val
                val = max(val,minValue(state.generateSuccessor(0, action), depth,  1))
                self.s +=1
               
            # terminates if value of val has not been changed i.e. there are no legalMoves left
            if prevVal== val:
                return self.evaluationFunction(state)

           
            return val
        

        # for pacman's first move
        val=float('-inf')
        bestaction = Directions.STOP
    
        for action in gameState.getLegalActions(0):
            prevVal=val
            # finds max value for pacman and assigns it to val
            val = max(val, minValue(gameState.generateSuccessor(0, action), self.depth, 1))

            # assigns action till there no LegalMoves left for pacman
            if val > prevVal:
                bestaction = action
        
        return bestaction

        print s

        

        util.raiseNotDefined()
   

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
       

        def minValue(state, depth, agentIndex, alpha, beta):
            
            # reassigns agentIndex to 0 if all the players has played and next is pacman's move
            if agentIndex == state.getNumAgents():
                return maxValue(state, depth - 1, alpha, beta)

            # initializes val to +infinity
            val = float('inf')
            prevVal=val
            
            # gets legalActions for the agentIndex
            legalMoves=[]            
            legalMoves = state.getLegalActions(agentIndex)
            
            for action in legalMoves:
                # finds min value for the agent and assigns it to val
                val= min(val,minValue(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta))

                # returns val if it is less than alpha
                if val < alpha:
                    return val
                                
                # replaces beta with current min value          
                beta=min(beta, val)
                
            # terminates if value of val has not been changed i.e. there are no legalMoves left   
            if prevVal== val:
                return self.evaluationFunction(state)

            
            return val

        def maxValue(state, depth, alpha, beta):
            
            # terminates if we have reached the bottom
            if depth ==0 :
                return self.evaluationFunction(state)
            
            # initializes val to +infinity
            val = float('-inf')
            prevVal=val
            
            # gets legalActions for pacman
            legalMoves=[]                     
            legalMoves = state.getLegalActions()
            
            for action in legalMoves:
                # finds max value for pacman and assigns it to val
                val = max(val,minValue(state.generateSuccessor(0, action), depth,  1, alpha, beta))
               

                # returns val if it is greater than beta
                if val > beta:
                    return val

                # replaces alpha with current max value 
                alpha = max(alpha, val)

            # terminates if value of val has not been changed i.e. there are no legalMoves left
            if prevVal== val:
                return self.evaluationFunction(state)

           
            return val
        

        #for pacman's first move
        alpha = float('-inf')
        beta = float('inf')
        val=float('-inf')
        bestaction = Directions.STOP
        for action in gameState.getLegalActions(0):
            prevVal=val
            # finds max value for pacman and assigns it to val
            val = max(val, minValue(gameState.generateSuccessor(0, action), self.depth, 1, alpha, beta))
            
            # assigns action till there no LegalMoves left for pacman
            if val > prevVal:
                bestaction = action
            
            if val >= beta:
                return bestaction
            alpha = max(alpha, val)

        return bestaction




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
        def minValue(state, depth, agentIndex):
            
            # reassigns agentIndex to 0 if all the players has played and next is pacman's move
            if agentIndex == state.getNumAgents():
                return maxValue(state, depth - 1)

            # initializes val to +infinity
            val = float('inf')
            prevVal=val
            
            # gets legalActions for the agentIndex
            legalMoves=[]            
            legalMoves = state.getLegalActions(agentIndex)
            
            expVal=0.0
            if len(legalMoves)!=0:
                prob=1.0/len(legalMoves)
                        
                                                                                
            for action in legalMoves:
                # finds min value for the agent and calculates the expected value
                val= minValue(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
                expVal+=prob*val
            
            
            # terminates if value of val has not been changed i.e. there are no more legalMoves left   
            if prevVal== val:
                return self.evaluationFunction(state)

            
            return expVal

        def maxValue(state, depth):
            
            #terminal state check
            if depth ==0 :
                return self.evaluationFunction(state)
            
            # initializes val to -infinity
            val = float('-inf')
            prevVal=val
            
            # gets legalActions for the agentIndex
            legalMoves=[]                     
            legalMoves = state.getLegalActions()
            
            for action in legalMoves:
                # finds max value for the agent and assigns it to val
                val = max(val,minValue(state.generateSuccessor(0, action), depth,  1))
                
               
            # terminates if value of val has not been changed i.e. there are no more legalMoves left    
            if prevVal== val:
                return self.evaluationFunction(state)

           
            return val
        

        #for pacman's first move
        val=float('-inf')
        bestaction = Directions.STOP
        for action in gameState.getLegalActions(0):
            prevVal=val
            # finds max value for pacman and assigns it to val
            val = max(val, minValue(gameState.generateSuccessor(0, action), self.depth, 1))
            # assigns action till there no LegalMoves left for pacman
            if val > prevVal:
                bestaction = action
        return bestaction


        util.raiseNotDefined()

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

