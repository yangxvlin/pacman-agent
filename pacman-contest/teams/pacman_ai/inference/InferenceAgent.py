"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-1-22 13:59:52
Description: the agent to do probability inference of the opponent's agents
"""
import random

from captureAgents import CaptureAgent
from capture import Directions
import util
import teams.pacman_ai.utility as utility
from ghostAgents import RandomGhost
from teams.pacman_ai.inference.inference import JointParticleFilter, ParticleFilter
from capture import GameState


class InferenceAgent(CaptureAgent):
    """"An agent that tracks and displays its beliefs about ghost positions."""

    def __init__( self, index, timeForComputing=.1, inference = "ExactInference", observeEnable = True, elapseTimeEnable = True):
        super().__init__(index, timeForComputing=timeForComputing)
        # self.index = index
        self.game_state = None

        # try:
        #     self.inferenceType = util.lookup(inference, globals())
        # except Exception:
        #     self.inferenceType = util.lookup('inference.' + inference, globals())
        # self.inferenceType = JointParticleFilter
        self.inferenceType = ParticleFilter

        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        CaptureAgent.registerInitialState(self, gameState)

        self.game_state = gameState

        self.opponent_agent_indices = utility.get_opponents_agent_indices(self.game_state, self.index)
        ghostAgents = [RandomGhost(index) for index in self.opponent_agent_indices]
        # print("ghostAgents", list(map(lambda x: x.index, ghostAgents)))
        # print("self.index: ", self.index)
        self.inferenceModules = [self.inferenceType(a, self.index) for a in ghostAgents]

        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        # for ghost, inference_modules in zip(ghostAgents, self.inferenceModules):
        #     inference_modules.addGhostAgent(ghost)

        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    # def observationFunction(self, gameState):
    #     "Removes the ghost states from the gameState"
    #     agents = gameState.data.agentStates
    #     gameState.data.agentStates = [None if i in self.opponent_agent_indices else agents[i] for i in range(0, len(agents))]
    #     return gameState

    def getAction(self, gameState: GameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        # for i in range(0, 4):
        #     print(gameState.isOnRedTeam(i), gameState.data.agentStates[i])
        # print("InferenceAgent.getAction", gameState.getAgentDistances())

        for index, inf in enumerate(self.inferenceModules):
            # print("InferenceAgent.getAction", index, not self.firstMove and self.elapseTimeEnable)
            if not self.firstMove and self.elapseTimeEnable:
                inf.elapseTime(gameState)
            self.firstMove = False
            if self.observeEnable:
                inf.observe(gameState)
            self.ghostBeliefs[index] = inf.getBeliefDistribution()

        for i in range(0, gameState.getNumAgents() // 2):
            print(i, "most likely at:", self.ghostBeliefs[i].argMax())
            print(self.ghostBeliefs[i])

        self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        # print("InferenceAgent.chooseAction", gameState.getAgentDistances())

        actions = gameState.getLegalActions(self.index)
        #
        # '''
        # You should change this in your own agent.
        # '''
        #
        # for i in range(0, 4):
        #     print(i, gameState.getAgentState(i))
        # print("InferenceAgent: self.index=", self.index, gameState.agentDistances)
        # # print(gameState.data.agentStates[0].configuration.getPosition())
        return random.choice(actions)
        # return Directions.STOP
