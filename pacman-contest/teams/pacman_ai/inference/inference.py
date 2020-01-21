# inference.py
# ------------
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


import game
import util
import teams.pacman_ai.utility as utility
from capture import GameState

from util import manhattanDistance, raiseNotDefined


class DiscreteDistribution(dict):
    """
    A DiscreteDistribution models belief distributions and weight distributions
    over a finite set of discrete keys.
    """
    def __getitem__(self, key):
        self.setdefault(key, 0)
        return dict.__getitem__(self, key)

    def copy(self):
        """
        Return a copy of the distribution.
        """
        return DiscreteDistribution(dict.copy(self))

    def argMax(self):
        """
        Return the key with the highest value.
        """
        if len(self.keys()) == 0:
            return None
        all = list(self.items())
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def total(self):
        """
        Return the sum of values for all keys.
        """
        return float(sum(self.values()))

    def normalize(self):
        """
        Normalize the distribution such that the total value of all keys sums
        to 1. The ratio of values for all keys will remain the same. In the case
        where the total value of the distribution is 0, do nothing.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> dist.normalize()
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0)]
        >>> dist['e'] = 4
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0), ('e', 4)]
        >>> empty = DiscreteDistribution()
        >>> empty.normalize()
        >>> empty
        {}
        """
        "*** YOUR CODE HERE ***"
        total_value = self.total()

        if total_value != 0:
            for i in self:
                self[i] /= total_value

    def sample(self):
        """
        Draw a random sample from the distribution and return the key, weighted
        by the values associated with each key.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> N = 100000.0
        >>> samples = [dist.sample() for _ in range(int(N))]
        >>> round(samples.count('a') * 1.0/N, 1)  # proportion of 'a'
        0.2
        >>> round(samples.count('b') * 1.0/N, 1)
        0.4
        >>> round(samples.count('c') * 1.0/N, 1)
        0.4
        >>> round(samples.count('d') * 1.0/N, 1)
        0.0
        """
        "*** YOUR CODE HERE ***"
        self.normalize()
        keys, values = zip(*self.items())
        return util.sample(values, keys)


class InferenceModule:
    """
    An inference module tracks a belief distribution over a ghost's location.
    """
    ############################################
    # Useful methods for all inference modules #
    ############################################

    def __init__(self, opponent_agent, self_index):
        """
        Set the ghost agent for later access.
        """
        self.opponent_agent = opponent_agent
        self.opponent_index = opponent_agent.index
        self.obs = []  # most recent observation position
        self.self_index = self_index

    def getPositionDistributionHelper(self, gameState, pos, opponent_index, agent):
        """

        :param gameState:
        :param pos:
        :param opponent_index: the opponent index
        :param agent: opponent agent object
        :return:
        """
        # set position to be inferred for opponent
        try:
            gameState = self.set_opponent_position(gameState, pos, opponent_index)
        except TypeError:
            gameState = self.set_opponent_positions(gameState, pos)

        self_positions = utility.get_agents_position(gameState)
        opponent_position = gameState.getAgentPosition(opponent_index)  # The position you set
        dist = DiscreteDistribution()

        if opponent_position in self_positions:  # The opponent has been caught!
            dist[gameState.getInitialAgentPosition()] = 1.0
            return dist

        self_successor_positions = []
        for self_position in self_positions:
            self_successor_positions += game.Actions.getLegalNeighbors(self_position, gameState.getWalls())  # Positions self agents can move to
        if opponent_position in self_successor_positions:  # Ghost could get caught
            mult = 1.0 / float(len(self_successor_positions))
            dist[gameState.getInitialAgentPosition()] = mult
        else:
            mult = 0.0

        # distribution for the agent's action behavior.
        # Probably, I will just uniform distribution(ghostAgents.RandomGhost) for the opponent's agent for simplicity.
        actionDist = agent.getDistribution(gameState)

        for action, prob in actionDist.items():
            successorPosition = game.Actions.getSuccessor(opponent_position, action)
            if successorPosition in self_successor_positions:  # Ghost could get caught
                denom = float(len(actionDist))
                dist[gameState.getInitialAgentPosition()] += prob * (1.0 / denom) * (1.0 - mult)
                dist[successorPosition] = prob * ((denom - 1.0) / denom) * (1.0 - mult)
            else:
                dist[successorPosition] = prob * (1.0 - mult)
        return dist

    def getPositionDistribution(self, gameState, pos, opponent_index=None, opponent_agent=None):
        """
        Return a distribution over successor positions of the ghost from the
        given gameState. You must first place the ghost in the gameState, using
        setGhostPosition below.
        """
        if opponent_agent is None:
            opponent_agent = self.opponent_agent
        return self.getPositionDistributionHelper(gameState, pos, opponent_index, opponent_agent)

    def getObservationProb(self, noisyDistance, pacmanPosition, ghostPosition, game_state: GameState):
        """
        Return the probability P(noisyDistance | pacmanPosition, ghostPosition).
        """
        "*** YOUR CODE HERE ***"
        true_distance = manhattanDistance(pacmanPosition, ghostPosition)
        return game_state.getDistanceProb(true_distance, noisyDistance)

    def set_opponent_position(self, gameState, opponent_position, opponent_index):
        """
        Set the position of the ghost for this inference module to the specified
        position in the supplied gameState.

        Note that calling setGhostPosition does not change the position of the
        ghost in the GameState object used for tracking the true progression of
        the game.  The code in inference.py only ever receives a deep copy of
        the GameState object which is responsible for maintaining game state,
        not a reference to the original object.  Note also that the ghost
        distance observations are stored at the time the GameState object is
        created, so changing the position of the ghost will not affect the
        functioning of observe.
        """
        conf = game.Configuration(opponent_position, game.Directions.STOP)
        gameState.data.agentStates[opponent_index] = game.AgentState(conf, gameState.data.agentStates[opponent_index].isPacman)
        return gameState

    def set_opponent_positions(self, gameState, ghostPositions):
        """
        Sets the position of all ghosts to the values in ghostPositions.
        """
        raiseNotDefined()
        # for index, pos in enumerate(ghostPositions):
        #     conf = game.Configuration(pos, game.Directions.STOP)
        #     gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
        # return gameState

    def observe(self, gameState):
        """
        Collect the relevant noisy distance observation and pass it along.
        """
        distances = gameState.getAgentDistances()
        if len(distances) >= self.opponent_index:  # Check for missing observations
            obs = distances[self.opponent_index]
            self.obs = obs
            self.observeUpdate(obs, gameState)

    def initialize(self, gameState):
        """
        Initialize beliefs to a uniform distribution over all legal positions.
        """
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        self.allPositions = self.legalPositions + [self.getJailPosition()]
        self.initializeUniformly(gameState)

    ######################################
    # Methods that need to be overridden #
    ######################################

    def initializeUniformly(self, gameState):
        """
        Set the belief state to a uniform prior belief over all positions.
        """
        raise NotImplementedError

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the given distance observation and gameState.
        """
        raise NotImplementedError

    def elapseTime(self, gameState):
        """
        Predict beliefs for the next time step from a gameState.
        """
        raise NotImplementedError

    def getBeliefDistribution(self):
        """
        Return the agent's current belief state, a distribution over ghost
        locations conditioned on all evidence so far.
        """
        raise NotImplementedError


# class ExactInference(InferenceModule):
#     """
#     The exact dynamic inference module should use forward algorithm updates to
#     compute the exact belief function at each time step.
#     """
#     def initializeUniformly(self, gameState):
#         """
#         Begin with a uniform distribution over legal ghost positions (i.e., not
#         including the jail position).
#         """
#         self.beliefs = DiscreteDistribution()
#         for p in self.legalPositions:
#             self.beliefs[p] = 1.0
#         self.beliefs.normalize()
#
#     def observeUpdate(self, observation, gameState):
#         """
#         Update beliefs based on the distance observation and Pacman's position.
#
#         The observation is the noisy Manhattan distance to the ghost you are
#         tracking.
#
#         self.allPositions is a list of the possible ghost positions, including
#         the jail position. You should only consider positions that are in
#         self.allPositions.
#
#         The update model is not entirely stationary: it may depend on Pacman's
#         current position. However, this is not a problem, as Pacman's current
#         position is known.
#         """
#         "*** YOUR CODE HERE ***"
#         noisy_distance = observation
#         pacman_position = gameState.getPacmanPosition()
#         jail_position = self.getJailPosition()
#
#         for possible_ghost_position in self.beliefs:
#             p_noisy_distance_given_true_distance = self.getObservationProb(noisy_distance, pacman_position, possible_ghost_position, jail_position)
#             self.beliefs[possible_ghost_position] *= p_noisy_distance_given_true_distance
#
#         self.beliefs.normalize()
#
#     def elapseTime(self, gameState):
#         """
#         Predict beliefs in response to a time step passing from the current
#         state.
#
#         The transition model is not entirely stationary: it may depend on
#         Pacman's current position. However, this is not a problem, as Pacman's
#         current position is known.
#         """
#         "*** YOUR CODE HERE ***"
#         pacman_position = gameState.getPacmanPosition()
#
#         new_beliefs = DiscreteDistribution()
#
#         new_position_distribution_dictionary = {}
#         for position in self.allPositions:
#             new_position_distribution_dictionary[position] = self.getPositionDistribution(gameState, position)
#
#         for newPos in self.allPositions:
#             new_beliefs[newPos] = 0.0
#
#             for oldPos in self.allPositions:
#                 newPosDist = new_position_distribution_dictionary[oldPos]
#                 new_beliefs[newPos] += newPosDist[newPos] * self.beliefs[oldPos]
#
#         new_beliefs.normalize()
#         self.beliefs = new_beliefs
#
#     def getBeliefDistribution(self):
#         return self.beliefs


class ParticleFilter(InferenceModule):
    """
    A particle filter for approximately tracking a single ghost.
    """
    def __init__(self, opponent_agent, numParticles=300):
        InferenceModule.__init__(self, opponent_agent)
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def initializeUniformly(self, gameState):
        """
        Initialize a list of particles. Use self.numParticles for the number of
        particles. Use self.legalPositions for the legal board positions where
        a particle could be located. Particles should be evenly (not randomly)
        distributed across positions in order to ensure a uniform prior. Use
        self.particles for the list of particles.
        """
        self.particles = []
        "*** YOUR CODE HERE ***"
        num_legal_positions = len(self.legalPositions)

        for i in range(0, self.numParticles):
            self.particles.append(self.legalPositions[i % num_legal_positions])

    def observeUpdate(self, observation, gameState: GameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distance to the ghost you are
        tracking.

        There is one special case that a correct implementation must handle.
        When all particles receive zero weight, the list of particles should
        be reinitialized by calling initializeUniformly. The total method of
        the DiscreteDistribution may be useful.
        """
        "*** YOUR CODE HERE ***"
        noisy_distance = observation
        self_position = gameState.getAgentPosition(self.self_index)

        belief = self.getBeliefDistribution()
        for possible_ghost_position in self.allPositions:
            p_noisy_distance_given_true_distance = self.getObservationProb(noisy_distance, self_position, possible_ghost_position, gameState)
            belief[possible_ghost_position] *= p_noisy_distance_given_true_distance
        belief.normalize()
        belief_total = belief.total()

        if belief_total == 0:
            self.initializeUniformly(gameState)
        else:
            self.particles.clear()
            for _ in range(0, self.numParticles):
                sample = belief.sample()
                self.particles.append(sample)

    def elapseTime(self, gameState):
        """
        Sample each particle's next state based on its current state and the
        gameState.
        """
        "*** YOUR CODE HERE ***"
        new_position_distribution_dictionary = {}
        for position in self.allPositions:
            new_position_distribution_dictionary[position] = self.getPositionDistribution(gameState, position)

        for i, old_particle in enumerate(self.particles):
            self.particles[i] = new_position_distribution_dictionary[old_particle].sample()

    def getBeliefDistribution(self):
        """
        Return the agent's current belief state, a distribution over ghost
        locations conditioned on all evidence and time passage. This method
        essentially converts a list of particles into a belief distribution.
        
        This function should return a normalized distribution.
        """
        "*** YOUR CODE HERE ***"
        belief = DiscreteDistribution()

        for particle in self.particles:
            belief[particle] += 1

        belief.normalize()
        return belief


class JointParticleFilter(ParticleFilter):
    """
    JointParticleFilter tracks a joint distribution over tuples of all ghost
    positions.
    """
    def __init__(self, numParticles=600):
        self.setNumParticles(numParticles)

    def initialize(self, gameState: GameState):
        """
        Store information about the game, then initialize particles.
        """
        self.numGhosts = utility.get_opponents_agent_num(gameState, self.self_index)
        self.ghostAgents = []
        super().initialize(gameState)
        self.initializeUniformly(gameState)

    def initializeUniformly(self, gameState):
        """
        Initialize particles to be consistent with a uniform prior. Particles
        should be evenly distributed across positions in order to ensure a
        uniform prior.
        """
        self.particles = []
        "*** YOUR CODE HERE ***"
        num_legal_positions = len(self.legalPositions)
        for i in range(0, self.numParticles):
            ghosts_position_sample = []
            for _ in range(0, self.numGhosts):
                ghosts_position_sample.append(self.legalPositions[i % num_legal_positions])
            self.particles.append(tuple(ghosts_position_sample))

    def addGhostAgent(self, agent):
        """
        Each ghost agent is registered separately and stored (in case they are
        different).
        """
        self.ghostAgents.append(agent)

    def getJailPosition(self, i):
        return (2 * i + 1, 1)

    def observe(self, gameState):
        """
        Resample the set of particles using the likelihood of the noisy
        observations.
        """
        observation = gameState.getNoisyGhostDistances()
        self.observeUpdate(observation, gameState)

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distances to all ghosts you
        are tracking.

        There is one special case that a correct implementation must handle.
        When all particles receive zero weight, the list of particles should
        be reinitialized by calling initializeUniformly. The total method of
        the DiscreteDistribution may be useful.
        """
        "*** YOUR CODE HERE ***"
        def get_ghost_belief_distribution(ghost_index, particles):
            """
            Return the agent's current belief state, a distribution over ghost_i
            locations conditioned on all evidence and time passage. This method
            essentially converts a list of particles into a belief distribution.

            This function should return a normalized distribution.
            """
            belief = DiscreteDistribution()

            for particle in particles:
                belief[particle[ghost_index]] += 1

            belief.normalize()
            return belief

        noisy_distances = observation
        pacman_position = gameState.getPacmanPosition()
        new_particles = [[] for _ in range(0, self.numParticles)]

        for i in range(self.numGhosts):
            belief = get_ghost_belief_distribution(i, self.particles)
            # print(i, belief)
            jail_position = self.getJailPosition(i)
            noisy_distance = noisy_distances[i]

            for possible_ghost_position in self.legalPositions:
                p_noisy_distance_given_true_distance = self.getObservationProb(noisy_distance, pacman_position, possible_ghost_position, jail_position)
                belief[possible_ghost_position] *= p_noisy_distance_given_true_distance
            belief.normalize()
            belief_total = belief.total()

            if belief_total == 0:
                self.initializeUniformly(gameState)
                return
            else:
                for m in range(0, self.numParticles):
                    sample = belief.sample()
                    new_particles[m].append(sample)

        self.particles = list(map(lambda x: tuple(x), new_particles))

    def elapseTime(self, gameState):
        """
        Sample each particle's next state based on its current state and the
        gameState.
        """
        newParticles = []
        for oldParticle in self.particles:
            newParticle = list(oldParticle)  # A list of ghost positions

            # now loop through and update each entry in newParticle...
            "*** YOUR CODE HERE ***"
            for i in range(self.numGhosts):
                newPosDist = self.getPositionDistribution(gameState, oldParticle, i, self.ghostAgents[i])

                newParticle[i] = newPosDist.sample()

            """*** END YOUR CODE HERE ***"""
            newParticles.append(tuple(newParticle))
        self.particles = newParticles


# One JointInference module is shared globally across instances of MarginalInference
jointInference = JointParticleFilter()


class MarginalInference(InferenceModule):
    """
    A wrapper around the JointInference module that returns marginal beliefs
    about ghosts.
    """
    def initializeUniformly(self, gameState):
        """
        Set the belief state to an initial, prior value.
        """
        if self.opponent_index == 1:
            jointInference.initialize(gameState, self.legalPositions)
        jointInference.addGhostAgent(self.opponent_agent)

    def observe(self, gameState):
        """
        Update beliefs based on the given distance observation and gameState.
        """
        if self.opponent_index == 1:
            jointInference.observe(gameState)

    def elapseTime(self, gameState):
        """
        Predict beliefs for a time step elapsing from a gameState.
        """
        if self.opponent_index == 1:
            jointInference.elapseTime(gameState)

    def getBeliefDistribution(self):
        """
        Return the marginal belief over a particular ghost by summing out the
        others.
        """
        jointDistribution = jointInference.getBeliefDistribution()
        dist = DiscreteDistribution()
        for t, prob in jointDistribution.items():
            dist[t[self.opponent_index - 1]] += prob
        return dist
