"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-20 22:15:33
Description: some helper functions
"""

from capture import GameState


def get_agents_position(game_state: GameState):
    """

    :param game_state:
    :return: a dictionary of {agent_index: (x, y) position} pair
    """
    agents_position = {}

    for i in range(0, game_state.getNumAgents()):
        pos = game_state.getAgentPosition(i)

        if pos:
            agents_position[i] = pos

    return agents_position
