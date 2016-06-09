# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from ghostAgents import RandomGhost


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
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    foodDistance = [manhattanDistance(newPos, foodPos) for foodPos in oldFood.asList()]
    minFoodDistance = min(foodDistance)

    ghostsPositions = [ghost.getPosition() for ghost in newGhostStates]
    ghostsDistance = [manhattanDistance(newPos, ghostPos) for ghostPos in ghostsPositions]
    minGhostDistance = min(ghostsDistance)

    return 1/(minFoodDistance+0.1) - 1/(minGhostDistance+0.1)

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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    def isPacmanTurn(agentIndex):
      if agentIndex == 0:
        return True
      else:
        return False


    def minimax(gameState, it):
      numAgents = gameState.getNumAgents()
      agentIndex = it % numAgents
      limit = self.depth * numAgents

      if it == limit:
        return self.evaluationFunction(gameState)

      if gameState.isLose() or gameState.isWin():
        return self.evaluationFunction(gameState)

      actions = gameState.getLegalActions(agentIndex)
      successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
      scores = []

      for successor in successors:
        scores.append(minimax(successor, it+1))

      if isPacmanTurn(agentIndex):
        return max(scores)
      else:
        return min(scores)

    maxScore = float('-inf')
    maxAction = ''

    for action in gameState.getLegalActions(0):
      state =  gameState.generateSuccessor(0, action)
      score = minimax(state, 1)

      if score > maxScore:
        maxScore = score
        maxAction = action

    return maxAction

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def isPacmanTurn(agentIndex):
      if agentIndex == 0:
        return True
      else:
        return False


    def alphabeta(gameState, it, a, b):
      numAgents = gameState.getNumAgents()
      agentIndex = it % numAgents
      limit = self.depth * numAgents

      if it == limit:
        return self.evaluationFunction(gameState)

      if gameState.isLose() or gameState.isWin():
        return self.evaluationFunction(gameState)

      actions = gameState.getLegalActions(agentIndex)
      successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
      scores = []

      if isPacmanTurn(agentIndex):
        v = float('-inf')

        for successor in successors:
          v = max(v, alphabeta(successor, it+1, a, b))
          a = max(a, v)
          if b <= a:
            break

        return v

      else:
        v = float('inf')

        for successor in successors:
          v = min(v, alphabeta(successor, it+1, a, b))
          b = min(b, v)
          if b <= a:
            break

        return v

    maxScore = float('-inf')
    maxAction = ''

    for action in gameState.getLegalActions(0):
      state =  gameState.generateSuccessor(0, action)
      score = alphabeta(state, 1, float('-inf'), float('inf'))

      if score > maxScore:
        maxScore = score
        maxAction = action

    return maxAction

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
    def isPacmanTurn(agentIndex):
      if agentIndex == 0:
        return True
      else:
        return False


    def expectminimax(gameState, it):
      numAgents = gameState.getNumAgents()
      agentIndex = it % numAgents
      limit = self.depth * numAgents

      if it == limit:
        return self.evaluationFunction(gameState)

      if gameState.isLose() or gameState.isWin():
        return self.evaluationFunction(gameState)

      actions = gameState.getLegalActions(agentIndex)
      successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
      scores = []

      for successor in successors:
        scores.append(expectminimax(successor, it+1))

      if isPacmanTurn(agentIndex):
        return max(scores)
      else:
        return sum(scores) / len(scores)

    maxScore = float('-inf')
    maxAction = ''

    for action in gameState.getLegalActions(0):
      state =  gameState.generateSuccessor(0, action)
      score = expectminimax(state, 1)

      if score > maxScore:
        maxScore = score
        maxAction = action

    return maxAction

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"

  if currentGameState.isWin():
    return float('inf')

  if currentGameState.isLose():
    return float('-inf')

  score = scoreEvaluationFunction(currentGameState)

  # FOOD
  foods = currentGameState.getFood().asList()
  if len(foods):
    score += 1/len(foods)

  # FOOD DISTANCE
  foods = [manhattanDistance(currentGameState.getPacmanPosition(), food) for food in foods]
  score += 1000/max(foods)

  # CAPSULES
  capsules = currentGameState.getCapsules()
  if len(capsules):
    score += 100/len(capsules)

  # GHOSTS
  ghosts = currentGameState.getNumAgents() - 1
  score += 1/ghosts

  # DEAD END
  actions = currentGameState.getLegalActions()
  score -= 100/len(actions)

  return score


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
