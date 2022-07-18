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
import random
import util
import sys

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        '''
        First, I get the positions of the ghosts and the food. Then, I create an array
        with the manhattanDistance for every food item and every ghost.

        Staying on the same position is a bad move. So I return a negative infinite number.
        That way the score will never be the maximum one and therefore will not be
        chosen in getActions.

        If the ghost is next to me, I pretend that I have lost (returning a negative infinite number).
        Reaching a point when no food is left in the maze means that I have not touched any ghost
        up to this point and therefore won. So I return a positive infinite number.

        As a metric for the state, I add up the sum of the foodDistance and the number of foodItems left.
        However, the program crashes when I just sum them up. Therefore I had to reduce the size of the
        numbers. 1/value seems to do the trick.
        '''

        foodItems = newFood.asList()
        ghostPositions = successorGameState.getGhostPositions()
        foodDistance = []
        ghostDistance = []

        for foodItem in foodItems:
            foodDistance.append(manhattanDistance(foodItem, newPos))
            #print(manhattanDistance(foodItem, newPos))
        for ghostPosition in ghostPositions:
            ghostDistance.append(manhattanDistance(ghostPosition, newPos))

        if currentGameState.getPacmanPosition() == newPos:
            return(-(float("inf")))

        for dist in ghostDistance:
            if dist < 2:
                return (-(float("inf")))
        if len(foodDistance) == 0:
            return float("inf")
        return 1/sum(foodDistance) + 1/len(foodDistance)


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        '''
        maxValue and minValue are calling each other (building the tree)
        '''

        def maxValue(gameState, depth):
            Actions = gameState.getLegalActions(0)

            # Am i done? Then return
            if len(Actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return(self.evaluationFunction(gameState), None)
            value = -(float("inf"))
            returnAction = None

            for action in Actions:

                successorValue = minValue(
                    gameState.generateSuccessor(0, action), 1, depth)

                successorValue = successorValue[0]
                if(successorValue > value):
                    value, returnAction = successorValue, action

            return(value, returnAction)

        def minValue(gameState, agentID, depth):
            Actions = gameState.getLegalActions(agentID)
            if len(Actions) == 0:
                return(self.evaluationFunction(gameState), None)

            value = float("inf")
            returnAction = None
            for action in Actions:
                if(agentID == gameState.getNumAgents() - 1):
                    successorValue = maxValue(
                        gameState.generateSuccessor(agentID, action), depth + 1)
                else:

                    successorValue = minValue(gameState.generateSuccessor(
                        agentID, action), agentID+1, depth)
                successorValue = successorValue[0]
                if(successorValue < value):
                    value, returnAction = successorValue, action

            return(value, returnAction)

        maxValue = maxValue(gameState, 0)[1]
        return maxValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # a = best max option
        # b = best min option

        def max_value(gameState, depth, a, b):
            Actions = gameState.getLegalActions(0)
            # Am i done? Then return null
            if len(Actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)

            value = -(float("inf"))
            returnAction = None

            for action in Actions:
                successValue = min_value(
                    gameState.generateSuccessor(0, action), 1, depth, a, b)
                successValue = successValue[0]
                if value < successValue:
                    value, returnAction = successValue, action
                if value > b:
                    return (value, returnAction)
                a = max(a, value)
            return (value, returnAction)

        def min_value(gameState, agentID, depth, a, b):

            Actions = gameState.getLegalActions(
                agentID)
            if len(Actions) == 0:
                return (self.evaluationFunction(gameState), None)

            l = float("inf")
            Act = None
            for action in Actions:
                if (agentID == gameState.getNumAgents() - 1):
                    successValue = max_value(gameState.generateSuccessor(
                        agentID, action), depth + 1, a, b)
                else:
                    successValue = min_value(gameState.generateSuccessor(
                        agentID, action), agentID + 1, depth, a, b)
                successValue = successValue[0]
                if (successValue < l):
                    l, Act = successValue, action

                if (l < a):
                    return (l, Act)

                b = min(b, l)

            return(l, Act)

        a = -(float("inf"))
        b = float("inf")
        max_value = max_value(gameState, 0, a, b)[1]
        return max_value


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
        def expMaxAgent(gameState, agent_Index, depth=0):

            # legal Actions of the Agent we want to expMax
            legalActionList = gameState.getLegalActions(agent_Index)

            # print("AgentIndex" + str(agent_Index))
            # actual number of agents in gameState
            gameStateAgents = gameState.getNumAgents()
            gameStateAgentsIndex = gameStateAgents - 1
            print("num of game state agents!", gameStateAgents)
            #print("selfIndex", self.index)
            # if game is over or depth is equal to the given value return the default evalFunc
            if (gameState.isLose() or gameState.isWin() or depth == self.depth):
                return [self.evaluationFunction(gameState)]
            # if we are checking only for actual agent again, go one step deeper
            elif agent_Index == gameStateAgentsIndex:
                depth += 1
                childAgentIndex = self.index

            # else check the expMax for the next agent
            else:
                childAgentIndex = agent_Index + 1

            #if player(pos) == MAX: value = -infinity
            if agent_Index == self.index:
                value = -1000000000000000000000.0
            #if player(pos) == CHANCE: value = 0
            else:
                value = 0

            numOfAction = len(legalActionList)
            choosen_Action = None

            # for each possible action calculete the expMax value and keep the maximum value
            for possible_Action in legalActionList:
                successorGameState = gameState.generateSuccessor(
                    agent_Index, possible_Action)
                expected_Max = expMaxAgent(
                    successorGameState, childAgentIndex, depth)[0]

                if agent_Index == self.index:
                    if expected_Max > value:
                        #value, best_move = nxt_val, move
                        value = expected_Max
                        choosen_Action = possible_Action
                else:
                    #value = value + prob(move) * nxt_val
                    value = value + ((1.0/numOfAction) * expected_Max)
            # return the best value and the best action
            return value, choosen_Action

        # call expMax and return the best move
        bestScoreActionPair = expMaxAgent(gameState, self.index)
        bestScore = bestScoreActionPair[0]
        bestMove = bestScoreActionPair[1]
        return bestMove


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: We have five important states.
        The best case szenario is a win, so a win contributes the most.
        The score is imprtant to. It will be wighted 10k times.
        Food, capsules and good ghostes get calculated in game and
        the evaluation scales down, the closer they are.
        Bad ghosts are improtent, because they have to be avoided. But they can't run faster then Pacman.
    """
    "*** YOUR CODE HERE ***"
    pacman_Pos = currentGameState.getPacmanPosition()   # Pacmans position
    ghost_Pos = currentGameState.getGhostPositions()    # ghost positions
    ghost_States = currentGameState.getGhostStates()    # ghost states
    # durations of scare state
    scared_Times = [ghostState.scaredTimer for ghostState in ghost_States]
    # Number of available capsules
    numOfCapsules = len(currentGameState.getCapsules())
    food_List = currentGameState.getFood().asList()     # List with food positions
    # get number of available food pebbles
    numOfFood = currentGameState.getNumFood()

    # List with ghosts
    bad_Ghosts = []
    good_Ghosts = []

    # inital wights of the different scenarios
    total_reward = 0
    win_reward = 0
    lose_reward = 0
    score_reward = 0
    foodScore_reward = 0
    ghost_reward = 0

    if currentGameState.isWin():
        # best possible reward
        win_reward = 10000000000000000000000000000
    elif currentGameState.isLose():
        # worst possible reward
        lose_reward = -10000000000000000000000000000

    # wighted score is the reward für a good score. It is lowerd over time
    score_reward = 10000 * currentGameState.getScore()

    capsules = 10000000000/(numOfCapsules+1)

    for food in food_List:
        # The farther away the food is and the more there are, the lower the reward
        foodScore_reward += 50 / \
            (manhattanDistance(pacman_Pos, food)) * numOfFood

    for time in range(len(scared_Times)):
        if scared_Times[time] == 0:
            bad_Ghosts.append(ghost_Pos[time])
        else:
            good_Ghosts.append(ghost_Pos[time])

    # bad ghostes have i higher reward, when the are farer away
    for death in bad_Ghosts:
        ghost_reward += manhattanDistance(pacman_Pos, death)

    # near good ghostes have a higher reward, when they are close by
    for goodGhostIndex in range(len(good_Ghosts)):
        ghost_reward += 1 / \
            (((manhattanDistance(pacman_Pos,
             good_Ghosts[goodGhostIndex])) * scared_Times[goodGhostIndex])+1)

    # sum up all rewards
    total_reward = win_reward + lose_reward + score_reward + \
        capsules + foodScore_reward + ghost_reward
    return total_reward


# Abbreviation
better = betterEvaluationFunction
