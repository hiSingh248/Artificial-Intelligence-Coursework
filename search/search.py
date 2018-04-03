# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    initialNode = problem.getStartState()                                  #get the start position of pacman and keep in initialNode

    visited = []                                                           #for tracking the nodes that are explored/visited. Mutable values, hence the list

    visited.append(initialNode)                                            #append the initialNode in visited list
    
    dfs_stack = util.Stack()                                               #initialize the data structure used for DFS i.e Stack
    
    dfs_stack.push((initialNode, []))                                      #push the initial position of the pacman into the Stack
    
    while not dfs_stack.isEmpty():                                         #perform each step below until the stack is empty

        currentNode, actions = dfs_stack.pop()                             #pop the top most state of the pacman
        
        if problem.isGoalState(currentNode):                               #check if the current state is the goal state
            return actions

        for(nextNode,action, cost) in problem.getSuccessors(currentNode):  #if not a goal state check if the successor node is unvisited and push into the Stack
                if nextNode not in visited:
                    newCost = actions + [action]
                    dfs_stack.push((nextNode, newCost))
        visited.append(currentNode)                                        #Add the successor node in the visited list if not added yet 
        
    return actions
    util.raiseNotDefined()



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
   
    initialNode=problem.getStartState();                                    #get the start position of pacman and keep in initialNode
    visitedNodes=[]                                                         #for tracking the nodes that are explored/visited. Mutable values, hence the list
    traverse_Queue=util.Queue()                                             #initialize the data structure used for BFS i.e Queue
    traverse_Queue.push((initialNode,[]))                                   #push the initial position of the pacman into the Queue

    while traverse_Queue:
        currentNode,currentAction = traverse_Queue.pop()                    #traverse and pop the top most state of the pacman
        
        if (problem.isGoalState(currentNode)):                              #check if the current state is the goal state
           return currentAction
        else:            
            for item in problem.getSuccessors(currentNode):                 #check if the successor node is unvisited and push into the Queue
                if item[0] not in visitedNodes:
                    nextAction= currentAction+[item[1]]                     
                    traverse_Queue.push((item[0],nextAction))                    
                    visitedNodes.append(item[0])

            if currentNode[0] not in visitedNodes:                          #Add the successor node in the visited list, if not added yet
                visitedNodes.append(currentNode[0])
                
            
    return []
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    initialNode = problem.getStartState()                                                   #get the start position of pacman and keep in initialNode
    visited = []                                                                            #for tracking the nodes that are explored/visited
    
    if problem.isGoalState(initialNode):                                                    #check if the initialState is the goal state
            return [] 

    
    ucs_pq = util.PriorityQueue()                                                           #Use priority queue as the data structure for UCS

    ucs_pq.push((initialNode,[]),0)                                                         #push the initialNode into the Queue  

    while not ucs_pq.isEmpty():                                                             #pop the current node state until the queeue is empty
        currentNode, actions = ucs_pq.pop()
        if problem.isGoalState(currentNode):
            return actions
        if currentNode not in visited:
            
            for(nextNode,action, cost) in problem.getSuccessors(currentNode):               
                if nextNode not in visited:
                    newCost = actions + [action]				            #for each node visited, add the cost of the path
                    ucs_pq.push((nextNode, newCost), problem.getCostOfActions(newCost))
        visited.append(currentNode)
    return actions
    util.raiseNotDefined()
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    initialNode=problem.getStartState();                                                    #get the Start position of the pacman and keep it in the initialNode
    visitedNodes=[]                                                                         #to keep the track of visited states/nodes
    traverse_PriorityQueue=util.PriorityQueue()                                             #Use priority Queue as data structure
    traverse_PriorityQueue.push((initialNode,[]),heuristic(initialNode,problem))            #push the node into the queu along with the heuristic information
      

    while traverse_PriorityQueue:
        currentNode,currentAction = traverse_PriorityQueue.pop()                            #pop the current state from the queue
       
        if (problem.isGoalState(currentNode)):                                              #check whether the current state is the goal state
           return currentAction
        
        if currentNode not in visitedNodes:
            visitedNodes.append(currentNode)
            for item in problem.getSuccessors(currentNode):                                 #visit the successors of the current state 
                if item[0] not in visitedNodes:                    
                    nextAction= currentAction+[item[1]]                    
                    fCost=problem.getCostOfActions(nextAction)+heuristic(item[0],problem)   #add the cost and the hueristic value of the path
                    traverse_PriorityQueue.push((item[0],nextAction),fCost)                 #push the total cost into the queue
                    visitedNodes.append(item)                                               #add the visited state in the list
                
            
    return []
    util.raiseNotDefined()
 




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
