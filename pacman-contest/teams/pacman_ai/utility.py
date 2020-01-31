"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-20 22:15:33
Description: some helper functions
"""

from capture import GameState, halfGrid
from teams.pacman_ai.constant import DELTA, NUM_DIRECTIONS
from collections import defaultdict
from util import Stack


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


def calculate_dead_end(movable_list, neighbors):
    """
    :param movable_list:
    :param neighbors:
    :return: {location: position to move to location} of a series of location in dead_ends
    """
    parent = {}  # parent means the dead end location (key) move from the parent[key] (value)
    stack = Stack()
    dead_ends = calculate_location_with_given_number_of_walls(movable_list, 3, neighbors)
    for dead_end in dead_ends:
        parent[dead_end] = None

        stack.push(dead_end)
        while not stack.isEmpty():
            loc = stack.pop()
            loc_neighbors = neighbors[loc]

            loc_neighbors_not_in_parent = list(filter(lambda x: x not in parent, loc_neighbors))

            if len(loc_neighbors_not_in_parent) == 1:
                the_neighbor_not_in_parent = loc_neighbors_not_in_parent[0]
                parent[loc] = the_neighbor_not_in_parent
                stack.push(the_neighbor_not_in_parent)

    return parent


def calculate_location_with_given_number_of_walls(all_locations, num_walls, neighbors):
    """
    :param all_locations:
    :param num_walls:
    :param neighbors: {position: [neighbor_position]}
    :return: location surrounded with given num_walls
    """
    res = []
    for location in all_locations:
        if len(neighbors[location]) == NUM_DIRECTIONS - num_walls:
            res.append(location)
    return res


def partition_location(game_state: GameState):
    """
    :param game_state:
    :return: not wall positions for red and blue respectively
    """
    red_movable = halfGrid(game_state.getWalls(), True).asList(False)
    blue_movable = halfGrid(game_state.getWalls(), False).asList(False)
    return red_movable, blue_movable


def tuple_add(x, y):
    """
    :param x: (a, b)
    :param y: (c, d)
    :return: (a+c, b+d)
    """
    return tuple(map(sum, zip(x, y)))


def get_neighbor(loc):
    """
    :param loc: a (x, y) location in game
    :return: a list of location
    """
    res = []
    for delta in DELTA:
        res.append(tuple_add(loc, delta))
    return res


def calculate_neighbors(game_state: GameState, locations):
    """
    :param game_state:
    :param locations:
    :return: the list of neighbor position of locations
    """
    neighbor = defaultdict(lambda: [])
    for location in locations:
        for location_neighbor in get_neighbor(location):
            if not game_state.hasWall(location_neighbor[0], location_neighbor[1]):
                neighbor[location].append(location_neighbor)
    return neighbor
