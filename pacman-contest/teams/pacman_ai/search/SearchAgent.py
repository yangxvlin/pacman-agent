"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-16 14:48:56
Description: contains agent for "Heuristic Search Algorithms (using general or pacman specific heuristic functions)"
"""

from teams.pacman_ai.BasicAgent import BasicAgent
import teams.pacman_ai.utility as utility
from teams.pacman_ai.constant import POSITIVE_INFINITY, OFFENSIVE_PREPARATION, OFFENSIVE, RETURN, DEFAULT_FOOD_PACK_NUM
import random
from capture import GameState
from captureAgents import CaptureAgent
from util import Counter, Stack, PriorityQueue, manhattanDistance
from game import Directions
import collections


class SearchAgent(BasicAgent):
    """
    A Search agent:
    """

    FOOD_TARGET = {}

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
        self.task_state = Stack()
        self.task_state.push(OFFENSIVE_PREPARATION)

        self.food_pack_num = DEFAULT_FOOD_PACK_NUM

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

        # code to test initial offensive target
        # print(self.index, self.INITIAL_TARGET[self.index], self.INITIAL_TARGET)

        agent_position = gameState.getAgentPosition(self.index)
        agent_food_packed = utility.get_agent_num_food_packed(gameState, self.index)
        current_task = self.task_state.list[-1]
        print(self.index, current_task)

        if current_task == OFFENSIVE_PREPARATION:
            # OFFENSIVE_PREPARATION not finished yet (i.e. not reach target nor becomes pacman)
            if agent_position != self.INITIAL_TARGET[self.index] and not gameState.getAgentState(self.index).isPacman:
                    next_position = greedy_maze_distance(self, agent_position, self.INITIAL_TARGET[self.index])
                    return utility.position_to_direction(agent_position, next_position)
            # becomes pacman before reach the target or reach the target, starts OFFENSIVE task
            else:
                self.task_state.pop()
                self.task_state.push(OFFENSIVE)
                return offensive_food_selection(gameState, self, agent_position, self.index)

        elif current_task == OFFENSIVE:
            next_action = None

            # enough food packed, time to return
            if agent_food_packed >= self.food_pack_num:
                # however still has chance to eat easy food, so try to eat it
                # continue to eat adjacent food might cause death, so give up this strategy currently
                # if utility.is_adjacent_to_food(gameState, agent_position):
                #     next_action = offensive_food_selection(gameState, self, agent_position, self.index)  # OFFENSIVE eat food
                #     # no food can eat, RETURN
                #     if not next_action:
                #         self.task_state.push(RETURN)
                #         return return_path_selection_pure_fabric(gameState, self, agent_position, self.index, self.get_self_boundary())
                #
                #     adj_foods = utility.get_adjacent_food(gameState, agent_position)
                #     next_position = utility.get_action_result(agent_position, next_action)
                #
                #     # goes to eat additional food
                #     if next_position in adj_foods:
                #         self.food_pack_num += 1
                #         return next_action
                #
                #     # not eating the adj_foods, so RETURN
                #     else:
                #         self.task_state.push(RETURN)
                #         return return_path_selection_pure_fabric(gameState, self, agent_position, self.index, self.get_self_boundary())
                #
                # find a path to RETURN
                # else:
                #     self.task_state.push(RETURN)
                #     return return_path_selection_pure_fabric(gameState, self, agent_position, self.index, self.get_self_boundary())

                self.task_state.push(RETURN)
                return return_path_selection_pure_fabric(gameState, self, agent_position, self.index, self.get_self_boundary())

            # try to eat food
            if not next_action:
                next_action = offensive_food_selection(gameState, self, agent_position, self.index)  # OFFENSIVE eat food
            # no path to eat food, so RETURN
            if not next_action:
                self.task_state.push(RETURN)
                next_action = return_path_selection_pure_fabric(gameState, self, agent_position, self.index, self.get_self_boundary())
            return next_action

        elif current_task == RETURN:
            # returned TODO reassess task to do
            if agent_position in self.get_self_boundary():
                next_action = offensive_food_selection(gameState, self, agent_position, self.index)  # OFFENSIVE eat food
                if next_action:
                    self.task_state.pop()
                    self.food_pack_num = min(DEFAULT_FOOD_PACK_NUM, self.getFood(gameState).count())
                    return next_action
                else:
                    # TODO defense
                    return Directions.STOP
            # not returned yet
            else:
                next_action = return_path_selection_pure_fabric(gameState, self, agent_position, self.index, self.get_self_boundary())
            return next_action

        # Note: when no food selection, so food not targeted
        # self.FOOD_TARGET[self.index] = None
        return Directions.STOP
        # return random.choice(actions)


def offensive_food_selection(game_state: GameState, agent: SearchAgent, agent_position, agent_index):
    foods = agent.getFood(game_state).asList()
    foods = sorted(foods, key=lambda x: agent.getMazeDistance(agent_position, x))

    for food in foods:
        dist_to_food = agent.getMazeDistance(agent_position, food)
        dist_to_closest_ghost = utility.get_opponents_ghosts_min_dist(game_state, agent_index, agent, agent_position)
        path_to_food = a_star_path(game_state,
                                   agent_position,
                                   [food],
                                   utility.get_opponents_ghosts_positions(game_state, agent_index),
                                   agent.neighbors,
                                   agent,
                                   1,
                                   1,
                                   1)

        # food in unreachable
        if not path_to_food:
            continue

        agent_next_position = utility.get_action_result(agent_position, path_to_food[0])

        # too danger to eat the food
        # food and agent in the same dead end path, danger to enter the dead end path if 2 * dist_to_food >= dist_to_closest_ghost
        # TODO some problems in this condition
        next_dist_to_food = agent.getMazeDistance(agent_next_position, food)
        if agent_next_position in agent.dead_end_path_length and food in agent.dead_end_path_length and \
                dist_to_food + agent.dead_end_path_length[food] >= dist_to_closest_ghost and \
                utility.is_in_the_same_dead_end_path(agent.dead_end_path, agent_next_position, food):
            continue

        # lock the target food for the agent
        if utility.is_food_locked(food, agent_index, agent, game_state, 3):
            continue
        agent.FOOD_TARGET[agent_index] = food

        return path_to_food[0]


def return_path_selection_pure_fabric(game_state: GameState, agent: SearchAgent, agent_position, agent_index, boundary):
    next_action = return_path_selection(game_state, agent, agent_position, agent_index, boundary)
    # has path to return
    if next_action:
        return next_action
    else:
        print("no path to return")
        return Directions.STOP


def return_path_selection(game_state: GameState, agent: SearchAgent, agent_position, agent_index, boundary):
    # no food selection, so food not targeted
    agent.FOOD_TARGET[agent_index] = None
    ghosts_positions = utility.get_opponents_ghosts_positions(game_state, agent_index)

    return_to_boundary_path = a_star_path(game_state,
                                          agent_position,
                                          boundary,
                                          ghosts_positions,
                                          agent.neighbors,
                                          agent,
                                          1,
                                          1,
                                          1)

    # has path to self boundary
    if return_to_boundary_path:
        return return_to_boundary_path[0]

    # no path to return, so eat capsule
    capsules = agent.getCapsules(game_state)
    if capsules:
        eat_capsule_path = a_star_path(game_state,
                                       agent_position,
                                       capsules,
                                       ghosts_positions,
                                       agent.neighbors,
                                       agent,
                                       1,
                                       1,
                                       1)
        if eat_capsule_path:
            return eat_capsule_path[0]

    # TODO no path to return or eat capsule so just leave as far as pacman can from ghosts
    print("no path to return " + str(agent_position))
    return Directions.STOP


# ******************************************************** pacman a star path search starts *******************************************************************
def back_track(goal_state, start_state, history):
    """
    :param goal_state:  goal
    :param start_state:  start
    :param history: a dictionary of {(x, y): (parent Position, direction from parent Position)}
    :return: a list of Direction from `start_state` to `goal_state`
    """
    result = []

    current_state = goal_state

    while hash(current_state) != hash(start_state):
        previous_state, previous_direction = history[current_state]
        result.append(previous_direction)
        current_state = previous_state

    return result[::-1]


def a_star_path(game_state: GameState, agent_position, targets: list, ghosts: dict, neighbors, agent: CaptureAgent, num_targets_to_reach=1, ghost_influence_range=0, step_cost=1):
    num_targets = len(targets)
    assert num_targets_to_reach <= num_targets
    opened_list = PriorityQueue()
    start_state = (agent_position, tuple(targets))
    opened_list.push(start_state, 0)  # {(agents_position, positions_to_go_to): priority}
    history = {}
    cost_so_far = collections.defaultdict(lambda: 0)

    while not opened_list.isEmpty():
        current_state = opened_list.pop()
        current_position, current_targets = current_state

        if num_targets - len(current_targets) == num_targets_to_reach:
            return back_track(current_position, agent_position, history)

        for next_step in _get_successors(game_state, current_position, current_targets, ghosts, neighbors, agent, ghost_influence_range, step_cost):
            next_state, next_direction, step_cost = next_step
            next_position, _ = next_state
            new_cost = cost_so_far[current_state] + step_cost

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                history[next_position] = (current_position, next_direction)
                priority = new_cost + _h2(next_state[0], next_state[1])
                opened_list.push(next_state, priority)
                cost_so_far[next_state] = new_cost


def _h2(start, goal_locations):
    """
    :param start: location to start
    :param goal_locations:  list of locations to go to
    :return: from start location to most far goal manhattan distance
    """
    result = [0]

    for goal in goal_locations:
        result.append(manhattanDistance(start, goal))
    return max(result)


def _get_successors(game_state: GameState, agent_position, targets: list, ghosts: dict, neighbors, agent: CaptureAgent, ghost_influence_range, step_cost):
    res = []

    for next_position in neighbors[agent_position]:
        # next_position is not in influenced area of ghosts or ghost is scared
        if all([utility.is_agent_scared(game_state, ghost_agent_index) or agent.getMazeDistance(next_position, ghost_position) > ghost_influence_range
                for ghost_agent_index, ghost_position in ghosts.items()]):
            if next_position not in targets:
                res.append(((next_position, targets), utility.position_to_direction(agent_position, next_position), step_cost))
            else:
                next_target = list(targets).copy()
                next_target.remove(next_position)
                res.append(((next_position, tuple(next_target)), utility.position_to_direction(agent_position, next_position), step_cost))
    return res


# ******************************************************** pacman a star path search ends *********************************************************************


def greedy_maze_distance(agent: BasicAgent, agent_position, agent_target):
    """
    :param agent:
    :param agent_position:
    :param agent_target:
    :return: choose next position to go based on pre-calculated maze-distance
    """
    next_position = None
    next_position_cost = POSITIVE_INFINITY

    for neighbor in agent.neighbors[agent_position]:
        if not next_position:
            next_position = neighbor
            next_position_cost = agent.getMazeDistance(neighbor, agent_target)
            continue

        tmp_next_position_cost = agent.getMazeDistance(neighbor, agent_target)
        if next_position_cost > tmp_next_position_cost:
            next_position = neighbor
            next_position_cost = tmp_next_position_cost

    return next_position


def alpha_beta(node: GameState, alpha, beta, evaluation_functions, current_player_index, team_indices, agent: CaptureAgent, depth=4):
    """
    modify from page 16: https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf
    :param node: game state
    :param alpha: alpha value
    :param beta: beta value
    :param evaluation_functions: {index: function} pair
    :param current_player_index: the playing player index
    :param team_indices: the agents' indices in one team
    :param agent: CaptureAgent object. used for calculating distance
    :param depth: depth cut-off
    :return: (action, evaluate score) pair
    """
    if node.isOver() or depth <= 0:
        if current_player_index in team_indices:
            return None, evaluation_functions[current_player_index](node, current_player_index, agent)
        else:
            return None, -evaluation_functions[current_player_index](node, current_player_index, agent)

    next_action = None

    next_player_index = utility.get_next_player_index(node, current_player_index)
    for action in node.getLegalActions(current_player_index):
        next_node = node.generateSuccessor(current_player_index, action)

        _, v = alpha_beta(next_node, -beta, -alpha, evaluation_functions, next_player_index, team_indices, agent, depth - 1)
        v *= -1

        if v > alpha:
            alpha = v
            next_action = action

        if alpha >= beta:
            return action, beta

    return next_action, alpha
