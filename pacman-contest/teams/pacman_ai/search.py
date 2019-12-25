# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

# ***************************** my code starts: *******************************


def back_track(goal_state, start_state, history):
    """
    :param goal_state:  goal
    :param start_state:  start
    :param history: a dictionary of {(x, y):
                            (parent Position, direction from parent Position)}
    :return: a list of Direction from `start_state` to `goal_state`
    """
    result = []

    current_state = goal_state

    while hash(current_state) != hash(start_state):
        previous_state, previous_direction = history[current_state]
        result.append(previous_direction)
        current_state = previous_state

    return result[::-1]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    opened_list = util.Stack()
    opened_list.push(problem.getStartState())
    closed_list = set()
    history = {}

    while not opened_list.isEmpty():
        current_state = opened_list.pop()

        if problem.isGoalState(current_state):
            return back_track(current_state, problem.getStartState(), history)

        closed_list.add(current_state)

        for next_step in problem.getSuccessors(current_state):
            next_state, next_direction, _ = next_step

            if next_state not in closed_list:
                opened_list.push(next_state)
                history[next_state] = (current_state, next_direction)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    opened_list = util.Queue()
    opened_list.push(problem.getStartState())

    history = {
        problem.getStartState(): (problem.getStartState(), Directions.STOP)}

    while not opened_list.isEmpty():
        current_state = opened_list.pop()

        if problem.isGoalState(current_state):
            return back_track(current_state, problem.getStartState(), history)

        for next_step in problem.getSuccessors(current_state):
            next_state, next_direction, _ = next_step

            if next_state not in history:
                opened_list.push(next_state)
                history[next_state] = (current_state, next_direction)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    import collections

    opened_list = util.PriorityQueue()
    opened_list.push(problem.getStartState(), 0)
    history = {
        problem.getStartState(): (problem.getStartState(), Directions.STOP)}
    cost_so_far = collections.defaultdict(lambda: 0)

    while not opened_list.isEmpty():
        current_state = opened_list.pop()

        if problem.isGoalState(current_state):
            return back_track(current_state, problem.getStartState(), history)

        for next_step in problem.getSuccessors(current_state):
            next_state, next_direction, step_cost = next_step
            new_cost = cost_so_far[current_state] + step_cost

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                history[next_state] = (current_state, next_direction)
                priority = new_cost + nullHeuristic(next_state, problem)
                opened_list.push(next_state, priority)
                cost_so_far[next_state] = new_cost


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    import collections

    opened_list = util.PriorityQueue()
    opened_list.push(problem.getStartState(), 0)
    history = {}
    cost_so_far = collections.defaultdict(lambda: 0)

    while not opened_list.isEmpty():
        current_state = opened_list.pop()

        if problem.isGoalState(current_state):
            return back_track(current_state, problem.getStartState(), history)

        for next_step in problem.getSuccessors(current_state):
            next_state, next_direction, step_cost = next_step
            new_cost = cost_so_far[current_state] + step_cost

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                history[next_state] = (current_state, next_direction)
                priority = new_cost + heuristic(next_state, problem)
                opened_list.push(next_state, priority)
                cost_so_far[next_state] = new_cost


def depth_limited_search(problem, depth_limit):
    opened_list = util.Stack()
    opened_list.push((problem.getStartState(), 1))
    closed_list = set()
    history = {}

    while not opened_list.isEmpty():
        current_state, depth = opened_list.pop()

        if problem.isGoalState(current_state):
            return back_track(current_state, problem.getStartState(), history)

        closed_list.add(current_state)

        if depth > depth_limit:
            continue

        for next_step in problem.getSuccessors(current_state):
            next_state, next_direction, _ = next_step

            if next_state not in closed_list:
                opened_list.push((next_state, depth+1))
                history[next_state] = (current_state, next_direction)

    return None


def iterative_deepening_search(problem):
    depth = 1

    while True:
        result = depth_limited_search(problem, depth)
        if result is not None:
            return result
        depth += 1


def weighted_a_star_search(problem, heuristic=nullHeuristic, weight=2):
    import collections

    opened_list = util.PriorityQueue()
    opened_list.push(problem.getStartState(), 0)
    history = {}
    cost_so_far = collections.defaultdict(lambda: 0)

    while not opened_list.isEmpty():
        current_state = opened_list.pop()

        if problem.isGoalState(current_state):
            return back_track(current_state, problem.getStartState(), history)

        for next_step in problem.getSuccessors(current_state):
            next_state, next_direction, step_cost = next_step
            new_cost = cost_so_far[current_state] + step_cost

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                history[next_state] = (current_state, next_direction)
                priority = new_cost + weight * heuristic(next_state, problem)
                opened_list.push(next_state, priority)
                cost_so_far[next_state] = new_cost


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterative_deepening_search
wastar = weighted_a_star_search
