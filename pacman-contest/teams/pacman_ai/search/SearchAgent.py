"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-16 14:48:56
Description: contains agent for "Heuristic Search Algorithms (using general or pacman specific heuristic functions)"
"""

from teams.pacman_ai.BasicAgent import BasicAgent
import random
from capture import GameState
from captureAgents import CaptureAgent
import teams.pacman_ai.utility as utility
from util import Counter


class SearchAgent(BasicAgent):
    """
    A Search agent:
    """

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
        super().registerInitialState(gameState)

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
        # code to test dead end calculation
        # dist = Counter({key: 1 for key in self.dead_end_path})
        # self.displayDistributionsOverPositions([dist])

        for i in range(0, 4):
            print(i, gameState.getAgentState(i))
        # print("SearchAgent: self.index=", self.index, gameState.agentDistances)
        # print(gameState.data.agentStates[0].configuration.getPosition())
        # return Directions.STOP
        return random.choice(actions)


def alpha_beta(node: GameState, alpha, beta, evaluation_functions, current_player_index, team_indices, search_agent: CaptureAgent, depth=4):
    """
    modify from page 16: https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf
    :param node: game state
    :param alpha: alpha value
    :param beta: beta value
    :param evaluation_functions: {index: function} pair
    :param current_player_index: the playing player index
    :param team_indices: the agents' indices in one team
    :param search_agent: CaptureAgent object. used for calculating distance
    :param depth: depth cut-off
    :return: (action, evaluate score) pair
    """
    if node.isOver() or depth <= 0:
        if current_player_index in team_indices:
            return None, evaluation_functions[current_player_index](node, current_player_index, search_agent)
        else:
            return None, -evaluation_functions[current_player_index](node, current_player_index, search_agent)

    next_action = None

    next_player_index = utility.get_next_player_index(node, current_player_index)
    for action in node.getLegalActions(current_player_index):
        next_node = node.generateSuccessor(current_player_index, action)

        _, v = alpha_beta(next_node, -beta, -alpha, evaluation_functions, next_player_index, team_indices, search_agent, depth-1)
        v *= -1

        if v > alpha:
            alpha = v
            next_action = action

        if alpha >= beta:
            return action, beta

    return next_action, alpha
