"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-16 14:48:56
Description: contains agent for "Heuristic Search Algorithms (using general or pacman specific heuristic functions)"
"""

from captureAgents import CaptureAgent
import random


class SearchAgent(CaptureAgent):
    """
    A Search agent:
    """

    def __init__(self, index, timeForComputing=.1):
        super().__init__(index, timeForComputing=.1)
        self.game_state = None

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

        '''
        Your initialization code goes here, if you need any.
        '''
        self.game_state = gameState

        # print(self.getCapsulesYouAreDefending(self.game_state))
        #
        # print(self.game_state.teams)
        #
        # print(self.red)
        #
        # print(self.getTeam(self.game_state))
        #
        # print(self.getOpponents(self.game_state))

        # print(gameState.getAgentState(1))

    def chooseAction(self, gameState):
        """
        Picks action based on the search result.
        """
        actions = gameState.getLegalActions(self.index)

        '''
        You should change this in your own agent.
        '''

        # for i in range(0, 4):
        #     print(i, gameState.getAgentState(i))
        # print(self.index, gameState.agentDistances)
        print(gameState.data.agentStates[0].configuration.getPosition())
        return random.choice(actions)

