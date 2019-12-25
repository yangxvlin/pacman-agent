"""
Author:      XuLin Yang
Student id:  904904
Date:        
Description: some helper functions to be used
"""

import teams.pacman_ai.search as search
from teams.pacman_ai.searchAgents import PositionSearchProblem


def manhattan_distance(xy1, xy2):
    """
    :param xy1: position 1 in terms of a tuple of two int
    :param xy2: position 2 in terms of a tuple of two int
    :return: The Manhattan distance for two position
    """
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclidean_distance(xy1, xy2):
    """
    :param xy1: position 1 in terms of a tuple of two int
    :param xy2: position 2 in terms of a tuple of two int
    :return: The Euclidean distance for two position
    """
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


def maze_distance(xy1, xy2, game_state):
    """
    :param xy1: position 1 in terms of a tuple of two int
    :param xy2: position 2 in terms of a tuple of two int
    :param game_state: The gameState can be any game state -- Pacman's position
                      in that state is ignored.
    :return: the maze distance between any two points, using the search function
    bfs.

    Example usage: mazeDistance( (2,4), (5,6), gameState)
    """
    x1, y1 = xy1
    x2, y2 = xy2
    walls = game_state.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(xy1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(xy2)
    prob = PositionSearchProblem(game_state, start=xy1, goal=xy2, warn=False, visualize=False)
    return len(search.bfs(prob))
