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


def get_opponents_agent_num(game_state: GameState, agent_index):
    """

    :param game_state:
    :param agent_index: self agent
    :return: number of agents in the opponent's team
    """
    if game_state.isOnRedTeam(agent_index):
        return len(game_state.getBlueTeamIndices())
    else:
        return len(game_state.getRedTeamIndices())


def get_opponents_agent_indices(game_state: GameState, agent_index):
    """

    :param game_state:
    :param agent_index: self agent
    :return: number of agents in the opponent's team
    """
    if game_state.isOnRedTeam(agent_index):
        return game_state.getBlueTeamIndices()
    else:
        return game_state.getRedTeamIndices()
