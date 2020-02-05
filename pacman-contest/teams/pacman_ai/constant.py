"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-28 15:38:54
Description: some constants used
"""

from game import Directions


""" negative infinity used in program """
NEGATIVE_INFINITY = float('-inf')

""" positive infinity used in program """
POSITIVE_INFINITY = float('inf')

""" moving in four directions """
DELTA = ((0, 1), (1, 0), (0, -1), (-1, 0))

""" direction w.r.t. DELTA """
DELTA_DIRECTION = (Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST)

""" number of legal directions """
NUM_DIRECTIONS = 4

""" default number of foods to be packed on the pacman """
DEFAULT_FOOD_PACK_NUM = 3

# ******************************************************* hand coded decision tree state starts ***************************************************************
""" the state to let agent to move to the calculated boundary position """
OFFENSIVE_PREPARATION = "offensive preparation"

""" the state that the agent invade into opponent's side and eat food """
OFFENSIVE = "offensive"

# ******************************************************* hand coded decision tree state ends *****************************************************************
