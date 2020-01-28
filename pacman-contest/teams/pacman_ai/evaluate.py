"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-28 16:35:56
Description: evaluation functions to be used
"""

from capture import GameState
from captureAgents import CaptureAgent
import teams.pacman_ai.utility as utility
from teams.pacman_ai.constant import POSITIVE_INFINITY, NEGATIVE_INFINITY


def score_evaluation(game_state: GameState, agent_index, search_agent: CaptureAgent):
    """
    :param game_state:
    :param agent_index: playing player's index
    :param search_agent: CaptureAgent to get mazeDistance
    :return: a positive value means player's leading scores
    """
    score = game_state.getScore()
    delta = 1
    if not game_state.isOnRedTeam(agent_index):
        delta = -1
    return delta * score


def opponent_ghost_distance_evaluation(game_state: GameState, agent_index, search_agent: CaptureAgent):
    """
    :param game_state:
    :param agent_index: playing player's index
    :param search_agent: CaptureAgent to get mazeDistance
    :return: evaluate how far is the agent from opponents ghosts
    """
    opponent_ghost_positions = utility.get_opponents_ghosts_positions(game_state, agent_index)
    if opponent_ghost_positions:
        agent_position = game_state.getAgentPosition(agent_index)
        max_dist = NEGATIVE_INFINITY
        for ghost_pos in opponent_ghost_positions:
            max_dist = max(max_dist, search_agent.distancer.getDistance(ghost_pos, agent_position))
        return max_dist
    else:
        return POSITIVE_INFINITY


def opponent_pacman_distance_evaluation(game_state: GameState, agent_index, search_agent: CaptureAgent):
    """
    :param game_state:
    :param agent_index: playing player's index
    :param search_agent: CaptureAgent to get mazeDistance
    :return: evaluate how far is the agent from opponents pacman
    """
    opponent_ghost_positions = utility.get_opponents_ghosts_positions(game_state, agent_index)
    if opponent_ghost_positions:
        agent_position = game_state.getAgentPosition(agent_index)
        max_dist = NEGATIVE_INFINITY
        for ghost_pos in opponent_ghost_positions:
            max_dist = max(max_dist, search_agent.distancer.getDistance(ghost_pos, agent_position))
        return max_dist
    else:
        return POSITIVE_INFINITY
