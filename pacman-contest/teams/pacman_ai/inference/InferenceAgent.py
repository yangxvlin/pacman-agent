"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-22 13:59:52
Description: the agent to do probability inference of the opponent's agents
"""

from captureAgents import CaptureAgent
from capture import Directions
import util
import teams.pacman_ai.utility as utility
from ghostAgents import RandomGhost

class InferenceAgent(CaptureAgent):
    """"An agent that tracks and displays its beliefs about ghost positions."""

    def __init__( self, index, timeForComputing=.1, inference = "ExactInference", observeEnable = True, elapseTimeEnable = True):
        super().__init__(index, timeForComputing=timeForComputing)
        self.game_state = None

        try:
            self.inferenceType = util.lookup(inference, globals())
        except Exception:
            self.inferenceType = util.lookup('inference.' + inference, globals())

        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        CaptureAgent.registerInitialState(self, gameState)

        self.game_state = gameState

        opponent_agent_indices = utility.get_opponents_agent_indices(self.game_state, self.index)
        ghostAgents = [RandomGhost(index) for index in opponent_agent_indices]
        self.inferenceModules = [self.inferenceType(a) for a in ghostAgents]

        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        for index, inf in enumerate(self.inferenceModules):
            if not self.firstMove and self.elapseTimeEnable:
                inf.elapseTime(gameState)
            self.firstMove = False
            if self.observeEnable:
                inf.observe(gameState)
            self.ghostBeliefs[index] = inf.getBeliefDistribution()
        self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP