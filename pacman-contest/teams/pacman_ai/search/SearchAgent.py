"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-16 14:48:56
Description: contains agent for "Heuristic Search Algorithms (using general or pacman specific heuristic functions)"
"""

from teams.pacman_ai.BasicAgent import BasicAgent
import teams.pacman_ai.utility as utility
from teams.pacman_ai.constant import POSITIVE_INFINITY, OFFENSIVE_PREPARATION, OFFENSIVE
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
        current_task = self.task_state.list[0]
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
            res = offensive_food_selection(gameState, self, agent_position, self.index)
            if res:
                return res

        # no food selection, so food not targeted
        self.FOOD_TARGET[self.index] = None
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
                                   1)

        # food in unreachable
        if not path_to_food:
            continue

        agent_next_position = utility.get_action_result(agent_position, path_to_food[0])

        # too danger to eat the food
        # food and agent in the same dead end path, danger to enter the dead end path if 2 * dist_to_food >= dist_to_closest_ghost
        if agent_next_position in agent.dead_end_path_length and food in agent.dead_end_path_length and 2 * dist_to_food > dist_to_closest_ghost-1 and \
                utility.is_in_the_same_dead_end_path(agent.dead_end_path, agent_next_position, food):
            continue

        # lock the target food for the agent
        if not utility.is_food_locked(food, agent_index, agent, game_state):
            agent.FOOD_TARGET[agent_index] = food

        return path_to_food[0]


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


def a_star_path(game_state: GameState, agent_position, targets: list, ghosts: dict, neighbors, agent: CaptureAgent, ghost_influence_range=0, step_cost=1):
    opened_list = PriorityQueue()
    start_state = (agent_position, tuple(targets))
    opened_list.push(start_state, 0)  # {(agents_position, positions_to_go_to): priority}
    history = {}
    cost_so_far = collections.defaultdict(lambda: 0)

    while not opened_list.isEmpty():
        current_state = opened_list.pop()
        current_position, current_targets = current_state

        if not current_targets:
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
