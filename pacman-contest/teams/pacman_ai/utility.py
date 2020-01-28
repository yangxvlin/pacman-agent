"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-20 22:15:33
Description: some helper functions
"""

from capture import GameState


def get_agents_positions(game_state: GameState, self_index):
    """

    :param self_index:
    :param game_state:
    :return: a dictionary of {agent_index: (x, y) position} pair
    """
    agents_position = {}

    for i in get_self_agent_indices(game_state, self_index):
        pos = game_state.getAgentPosition(i)

        if pos:
            agents_position[i] = pos

    return agents_position


def get_opponents_positions(game_state: GameState, agent_index):
    """
    :param game_state:
    :param agent_index: self agent
    :return: a dictionary of {opponent_agent_index: (x, y) position} pair
    """
    opponents_indices = get_opponents_agent_indices(game_state, agent_index)
    agents_position = {}

    for i in opponents_indices:
        pos = game_state.getAgentPosition(i)

        if pos:
            agents_position[i] = pos

    return agents_position


def are_opponents_ghosts(game_state: GameState, agent_index):
    """
    :param game_state:
    :param agent_index:
    :return: are opponent's agents are ghosts
    """
    for i in get_opponents_agent_indices(game_state, agent_index):
        if not is_agent_ghost(game_state, i):
            return False
    return True


def are_opponents_pacmans(game_state: GameState, agent_index):
    """
    :param game_state:
    :param agent_index:
    :return: are opponent's agents are pacman
    """
    for i in get_opponents_agent_indices(game_state, agent_index):
        if is_agent_ghost(game_state, i):
            return False
    return True


def get_opponents_ghosts_positions(game_state: GameState, agent_index):
    """
    :param game_state:
    :param agent_index:
    :return list of opponents ghosts position
    """
    positions = []
    for i in get_opponents_agent_indices(game_state, agent_index):
        if is_agent_ghost(game_state, i):
            positions.append(game_state.getAgentPosition(i))
    return positions


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


def get_self_agent_indices(game_state: GameState, agent_index):
    """

    :param game_state:
    :param agent_index: self agent
    :return: number of agents in the self team
    """
    if game_state.isOnRedTeam(agent_index):
        return game_state.getRedTeamIndices()
    else:
        return game_state.getBlueTeamIndices()


def get_next_player_index(game_state: GameState, agent_index):
    """
    :param game_state:
    :param agent_index: current playing player's index
    :return: next playing player's index
    """
    agent_index += 1
    if agent_index == game_state.getNumAgents():
        agent_index = 0
    return  agent_index


def is_agent_ghost(game_state: GameState, agent_index):
    return not game_state.getAgentState(agent_index).isPacman
