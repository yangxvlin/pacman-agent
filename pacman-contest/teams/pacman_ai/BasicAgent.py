"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-31 18:57:28
Description: the basic Agent to be extended
"""

from teams.pacman_ai.omniscient.OmniscientAgent import OmniscientAgent
import util
from captureAgents import CaptureAgent
import teams.pacman_ai.utility as utility
from capture import GameState


class BasicAgent(OmniscientAgent):
    INITIAL_TARGET = None

    def __init__(self, index, timeForComputing=.1):
        super().__init__(index, timeForComputing)

    def registerInitialState(self, gameState: GameState):
        super().registerInitialState(gameState)

        self.red_movable, self.blue_movable = utility.partition_location(gameState)
        self.all_movable = gameState.getWalls().asList(False)
        self.neighbors = utility.calculate_neighbors(gameState, self.all_movable)
        self.dead_end_path = utility.calculate_dead_end(self.all_movable, self.neighbors)
        self.red_boundary = utility.agent_boundary_calculation(self.red_movable, True)
        self.blue_boundary = utility.agent_boundary_calculation(self.blue_movable, False)

        if not BasicAgent.INITIAL_TARGET:
            if self.red:
                BasicAgent.INITIAL_TARGET = utility.initial_offensive_position_calculation(self.red_boundary,
                                                                                           self,
                                                                                           utility.get_agents_positions(gameState, self.index))
            else:
                BasicAgent.INITIAL_TARGET = utility.initial_offensive_position_calculation(self.blue_boundary,
                                                                                           self,
                                                                                           utility.get_agents_positions(gameState, self.index))

    def chooseAction(self, gameState):
        util.raiseNotDefined()
