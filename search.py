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

from typing import List, final
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

def getFinalPath(finalPath):
    from game import Directions
    s = Directions.SOUTH
    n = Directions.NORTH
    w = Directions.WEST
    e = Directions.EAST
    way = []
    #print("finalPath", finalPath)
    for node in finalPath:
        #print("finalPath", node)
        
        if node[1] == "South":
            way.append(s)
        elif node[1] == "North":
            way.append(n)
        elif node[1] == "West":
            way.append(w)
        elif node [1] == "East":
            way.append(e)
        else:
            continue
    return way

def getFinalPathWhole(finalPath):
    PathInWords = []
    for entry in finalPath:
        if not entry[1] == '':
            PathInWords.append(entry[1])            
    return PathInWords

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    #Path found
    # path = []
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    startState = problem.getStartState() #currentState is startingState at first

    # stack = util.Stack()
    visited = set()
    path = list()
    if problem.isGoalState(startState):
        return list()

   
    #dfs with rec. is saving path in 'actions' list
    diveDeeper(problem, visited, startState, path)
    return path

def diveDeeper(problem, visited, startNode, path):
       
    if problem.isGoalState(startNode):
        return True
    
    if startNode in visited:
        return False

    visited.add(startNode)
    successors = problem.getSuccessors(startNode)
    for nextNode in successors:
        path.append(nextNode[1])
        
        if diveDeeper(problem, visited, nextNode[0], path):
            return True
        path.pop()

    visited.remove(startNode)
    return False


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()

    if problem.isGoalState(startState):
        return list()
    
    visited = set()
    queue = util.Queue()
    #put root node in queue, where node is tuple(state, actions's list)
    
    queue.push((startState, list()))
    while not queue.isEmpty():
        currentNode = queue.pop()
        
        # check if goal state is reached
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]
        
        # check if goal state is visited
        if currentNode[0] in visited:
            continue
        
        visited.add(currentNode[0])
        # explore the next lvl states in queue which parent is curr
        successors = problem.getSuccessors(currentNode[0])
        for nextNode in successors:
            path = list(currentNode[1])
            path.append(nextNode[1])
            queue.push((nextNode[0],path))

    return list()

    #util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    startState = problem.getStartState()

    if problem.isGoalState(startState):
        return list()
    
    visited = set()
    queue = util.PriorityQueue()
    #put root node in queue, where node is tuple(state, actions's list)
    
    queue.push((startState, list(),0.0), 0.0)
    while not queue.isEmpty():
        currentNode = queue.pop()
        
        # check if goal state is reached
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]
        
        # check if goal state is visited
        if currentNode[0] in visited:
            continue
        
        visited.add(currentNode[0])
        # explore the next lvl states in queue which parent is curr
        successors = problem.getSuccessors(currentNode[0])
        for nextNode in successors:
            path = list(currentNode[1])
            path.append(nextNode[1])
            cost = currentNode[2] + nextNode[2]
            queue.push((nextNode[0],path, cost), cost)

    return list()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
   
    startState = problem.getStartState()

    if problem.isGoalState(startState):
        return list()
   
    closedList = set()
    openList = util.PriorityQueue()
    #put root node in queue, where node is tuple(state, actions's list, cost of path + heuristic)
    openList.push((startState,list(),0.0), 0.0)
    
    while not openList.isEmpty():
        currentNode = openList.pop()
        # check if goal state is reached
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]
        # check if goal state is visited
        if currentNode[0] in closedList:
            continue
        closedList.add(currentNode[0])
        # explore the next lvl states in queue which parent is curr
        
        successors = problem.getSuccessors(currentNode[0])
        for nextNode in successors:
            path = list(currentNode[1])
            path.append(nextNode[1])
            cost = currentNode[2]+nextNode[2]
            # push new node where priority is cost of path + heuristic of this node            
            openList.push((nextNode[0], path, cost), cost + heuristic(nextNode[0],problem))
    
    return list()



    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
