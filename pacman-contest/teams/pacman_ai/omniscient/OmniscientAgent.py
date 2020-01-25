"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-25 18:43:26
Description: an agent that hack the invisibility of the system that enable the agent to see the exact coordinates of the opponent's agents
"""

from captureAgents import CaptureAgent
from capture import GameState
import util


class OmniscientAgent(CaptureAgent):
    def __init__(self, index, timeForComputing=.1):
        super().__init__(index, timeForComputing)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent to populate useful fields (such as what team we're on).

        A distanceCalculator instance caches the maze distances between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 15 seconds.
        """

        '''
        Make sure you do not delete the following line. If you would like to use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        '''
        CaptureAgent.registerInitialState(self, gameState)

    def chooseAction(self, gameState):
        util.raiseNotDefined()

    def observationFunction(self, gameState: GameState):
        return self.makeObservation(gameState, self.index)

    def makeObservation(self, game_state: GameState, index):
        state = game_state.deepCopy()

        pos = state.getAgentPosition(index)
        n = state.getNumAgents()
        distances = [util.manhattanDistance(pos, state.getAgentPosition(i)) for i in range(n)]
        state.agentDistances = distances

        return state
