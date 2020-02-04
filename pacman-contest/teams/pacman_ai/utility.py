"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-20 22:15:33
Description: some helper functions
"""

from capture import GameState, halfGrid
from captureAgents import CaptureAgent
from teams.pacman_ai.constant import DELTA, DELTA_DIRECTION, NUM_DIRECTIONS, POSITIVE_INFINITY
from collections import defaultdict
from util import Stack
from game import Directions
import random


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
    :return dictionary of opponents ghosts position
    """
    positions = {}
    for i in get_opponents_agent_indices(game_state, agent_index):
        if is_agent_ghost(game_state, i):
            positions[i] = game_state.getAgentPosition(i)
    return positions


def get_opponents_ghosts_min_dist(game_state: GameState, agent_index, agent: CaptureAgent, agent_position):
    opponents_ghosts_positions = get_opponents_ghosts_positions(game_state, agent_index).values()
    if not opponents_ghosts_positions:
        return POSITIVE_INFINITY
    else:
        return min(list(map(lambda x: agent.getMazeDistance(agent_position, x), opponents_ghosts_positions)))


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
    return agent_index


def is_agent_ghost(game_state: GameState, agent_index):
    return not game_state.getAgentState(agent_index).isPacman


def is_agent_scared(game_state: GameState, agent_index):
    return game_state.getAgentState(agent_index).scaredTimer > 0


def get_action_result(agent_position, action):
    for delta, direction in zip(DELTA, DELTA_DIRECTION):
        if direction == action:
            return tuple_add(agent_position, delta)
    # otherwise the action is STOP
    assert action == Directions.STOP
    return agent_position


# ****************************************** dead end calculation start ***************************************************************************************
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
    width = game_state.getWalls().width
    height = game_state.getWalls().height
    halfway = width // 2

    red_movable = []
    blue_movable = []

    for x in range(0, width):
        for y in range(0, height):
            if game_state.hasWall(x, y):
                continue
            if x < halfway:
                red_movable.append((x, y))
            else:
                blue_movable.append((x, y))

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
# ****************************************** dead end calculation end *****************************************************************************************


def is_in_the_same_dead_end_path(dead_end_path, pos1, pos2):
    if pos1 not in dead_end_path or pos2 not in dead_end_path:
        return False

    pos1_source = pos1
    pos2_source = pos2

    while pos1_source in dead_end_path:
        pos1_source = dead_end_path[pos1_source]

    while pos2_source in dead_end_path:
        pos2_source = dead_end_path[pos2_source]

    return pos1_source == pos2_source


def agent_boundary_calculation(positions, is_red):
    # print(positions)
    xs = list(map(lambda x: x[0], positions))
    if is_red:
        max_x = max(xs)
        return list(filter(lambda x: x[0] == max_x, positions))
    else:
        min_x = min(xs)
        return list(filter(lambda x: x[0] == min_x, positions))


def initial_offensive_position_calculation(red_boundary_positions: list,
                                           blue_boundary_positions: list,
                                           agent: CaptureAgent,
                                           red_agents_position,
                                           blue_agents_position,
                                           game_state: GameState):
    from teams.pacman_ai.inference.inference import DiscreteDistribution

    red_boundary_positions_original = red_boundary_positions.copy()
    blue_boundary_positions_original = blue_boundary_positions.copy()
    targets = []

    for i in range(0, game_state.getNumAgents()):
        if game_state.isOnRedTeam(i):
            if i == 0:
                # assign closest boundary position to agent0
                min_dist = min([agent.getMazeDistance(red_agents_position[i], pos) for pos in red_boundary_positions])
                agent0_target = random.choice(list(filter(lambda x: agent.getMazeDistance(red_agents_position[i], x) == min_dist, red_boundary_positions)))
                red_boundary_positions.remove(agent0_target)
                targets.append(agent0_target)
            else:
                # no possible positions, start again
                if not red_boundary_positions:
                    red_boundary_positions = red_boundary_positions_original.copy()

                distribution = DiscreteDistribution()
                for pos in red_boundary_positions:
                    distribution[pos] = agent.getMazeDistance(red_agents_position[i], pos)
                distribution.normalize()
                agent_i_target = distribution.sample()
                targets.append(agent_i_target)
        else:
            if i == 1:
                # assign closest boundary position to agent0
                min_dist = min([agent.getMazeDistance(blue_agents_position[i], pos) for pos in blue_boundary_positions])
                agent0_target = random.choice(list(filter(lambda x: agent.getMazeDistance(blue_agents_position[i], x) == min_dist, blue_boundary_positions)))
                blue_boundary_positions.remove(agent0_target)
                targets.append(agent0_target)
            else:
                # no possible positions, start again
                if not blue_boundary_positions:
                    blue_boundary_positions = blue_boundary_positions_original.copy()

                distribution = DiscreteDistribution()
                for pos in blue_boundary_positions:
                    distribution[pos] = agent.getMazeDistance(blue_agents_position[i], pos)
                distribution.normalize()
                agent_i_target = distribution.sample()
                targets.append(agent_i_target)

    return targets

    # second_agent_index = max(agents_position)
    # first_agent_index = min(agents_position)
    # second_agent_position = agents_position[second_agent_index]
    # first_agent_position = agents_position[first_agent_index]
    #
    # min_dist = min([agent.getMazeDistance(second_agent_position, pos) for pos in boundary_positions])
    # second_agent_target = random.choice(list(filter(lambda x: agent.getMazeDistance(second_agent_position, x) == min_dist, boundary_positions)))
    #
    # boundary_positions.remove(second_agent_target)
    # distribution = DiscreteDistribution()
    # for pos in boundary_positions:
    #     assert pos != second_agent_target
    #     distribution[pos] = agent.getMazeDistance(first_agent_position, pos)
    # distribution.normalize()
    # first_agent_target = distribution.sample()
    #
    # return first_agent_target, second_agent_target


def position_to_direction(current_position, next_position):
    """
    :param current_position:
    :param next_position:
    :return: Directions from current_position to next_position
    """
    for delta, direction in zip(DELTA, DELTA_DIRECTION):
        if tuple_add(current_position, delta) == next_position:
            return direction
    return None


def closest_food(agent_position, game_state: GameState, is_red, agent: CaptureAgent):
    food = []
    if is_red:
        food = game_state.getBlueFood().asList()
    else:
        food = game_state.getRedFood().asList()

    min_dist = min([agent.getMazeDistance(agent_position, pos) for pos in food])
    chosen_food = random.choice(list(filter(lambda x: agent.getMazeDistance(agent_position, x) == min_dist, food)))

    return chosen_food
