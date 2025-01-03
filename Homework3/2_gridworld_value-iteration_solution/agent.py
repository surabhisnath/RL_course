import util, random
import numpy as np


class Agent:

    def getAction(self, state):
        """
        For the given state, get the agent's chosen
        action.  The agent knows the legal actions
        """
        abstract

    def getValue(self, state):
        """
        Get the value of the state.
        """
        abstract

    def getQValue(self, state, action):
        """
        Get the q-value of the state action pair.
        """
        abstract

    def getPolicy(self, state):
        """
        Get the policy recommendation for the state.

        May or may not be the same as "getAction".
        """
        abstract

    def update(self, state, action, nextState, reward):
        """
        Update the internal state of a learning agent
        according to the (state, action, nextState)
        transistion and the given reward.
        """
        abstract


class RandomAgent(Agent):
    """
    Clueless random agent, used only for testing.
    """

    def __init__(self, actionFunction):
        self.actionFunction = actionFunction

    def getAction(self, state):
        return random.choice(self.actionFunction(state))

    def getValue(self, state):
        return 0.0

    def getQValue(self, state, action):
        return 0.0

    def getPolicy(self, state):
        return "random"

    def update(self, state, action, nextState, reward):
        pass


################################################################################
# Exercise 2


class ValueIterationAgent(Agent):

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
        Your value iteration agent should take an mdp on
        construction, run the indicated number of iterations
        and then act according to the resulting policy.
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations

        states = self.mdp.getStates()
        number_states = len(states)

        self.V = {s: 0 for s in states}

        for i in range(iterations):
            newV = {}
            for s in states:
                actions = self.mdp.getPossibleActions(s)
                if len(actions) < 1:
                    newV[s] = 0.0
                else:
                    newV[s] = np.max([self.getQValue(s, a) for a in actions])
            self.V = newV

    def getValue(self, state):
        """
        Look up the value of the state (after the indicated
        number of value iteration passes).
        """
        return self.V[state]

    def getQValue(self, state, action):
        """
        Look up the q-value of the state action pair
        (after the indicated number of value iteration
        passes).  Note that value iteration does not
        necessarily create this quantity and you may have
        to derive it on the fly.
        """
        # get all successor states and probabilities and evaluate value of these states
        return self.mdp.getReward(state, action, None) + self.discount * np.sum(
            [
                self.V[sp] * prob
                for sp, prob in self.mdp.getTransitionStatesAndProbs(state, action)
            ]
        )

    def getPolicy(self, state):
        """
        Look up the policy's recommendation for the state
        (after the indicated number of value iteration passes).
        """
        # do greedy on Q
        actions = self.mdp.getPossibleActions(state)
        if len(actions) < 1:
            return None
        else:
            qValues = [self.getQValue(state, a) for a in actions]
            action_index = np.argmax(qValues)
            return actions[action_index]

    def getAction(self, state):
        """
        Return the action recommended by the policy.
        """
        return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        """
        Not used for value iteration agents!
        """

        pass


class PolicyIterationAgent(Agent):

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
        Your value iteration agent should take an mdp on
        construction, run the indicated number of iterations
        and then act according to the resulting policy.
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        threshold = 0.01

        states = self.mdp.getStates()

        self.V = {s: 0 for s in states}
        self.policy = {
            s: np.random.choice(self.mdp.getPossibleActions(s))
            for s in states
            if len(self.mdp.getPossibleActions(s)) > 0
        }  # initialise randomly

        it = 0
        print("Iteration:", it)
        print("Value:", self.V)
        print("Policy:", self.policy)

        while True:

            # policy evaluation
            while True:
                maxchange = 0
                for s in states:
                    if len(self.mdp.getPossibleActions(s)) != 0:
                        v_s = self.V[s]
                        self.V[s] = self.getQValue(s, self.policy[s])
                        maxchange = np.max([maxchange, np.abs(v_s - self.V[s])])
                if maxchange < threshold:
                    break

            # policy improvement
            policy_stable = True
            for s in states:
                if len(self.mdp.getPossibleActions(s)) != 0:
                    old_action = self.policy[s]
                    self.policy[s] = self.getPolicy(s)
                    if old_action != self.policy[s]:
                        policy_stable = False

            if policy_stable:
                break

            it += 1
            print("Iteration:", it)
            print("Value:", self.V)
            print("Policy:", self.policy)

    def getValue(self, state):
        """
        Look up the value of the state (after the indicated
        number of value iteration passes).
        """
        return self.V[state]

    def getQValue(self, state, action):
        """
        Look up the q-value of the state action pair
        (after the indicated number of value iteration
        passes).  Note that value iteration does not
        necessarily create this quantity and you may have
        to derive it on the fly.
        """
        # get all successor states and probabilities and evaluate value of these states
        return self.mdp.getReward(state, action, None) + self.discount * np.sum(
            [
                self.V[sp] * prob
                for sp, prob in self.mdp.getTransitionStatesAndProbs(state, action)
            ]
        )

    def getPolicy(self, state):
        """
        Look up the policy's recommendation for the state
        (after the indicated number of value iteration passes).
        """
        # do greedy on Q
        actions = self.mdp.getPossibleActions(state)
        if len(actions) < 1:
            return None
        else:
            qValues = [self.getQValue(state, a) for a in actions]
            action_index = np.argmax(qValues)
            return actions[action_index]

    def getAction(self, state):
        """
        Return the action recommended by the policy.
        """
        return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        """
        Not used for value iteration agents!
        """

        pass


# Below can be ignored for Exercise 2


class QLearningAgent(Agent):

    def __init__(self, actionFunction, discount=0.9, learningRate=0.1, epsilon=0.2):
        """
        A Q-Learning agent gets nothing about the mdp on
        construction other than a function mapping states to actions.
        The other parameters govern its exploration
        strategy and learning rate.
        """
        self.setLearningRate(learningRate)
        self.setEpsilon(epsilon)
        self.setDiscount(discount)
        self.actionFunction = actionFunction

        raise "Your code here."

    # THESE NEXT METHODS ARE NEEDED TO WIRE YOUR AGENT UP TO THE CRAWLER GUI

    def setLearningRate(self, learningRate):
        self.learningRate = learningRate

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setDiscount(self, discount):
        self.discount = discount

    # GENERAL RL AGENT METHODS

    def getValue(self, state):
        """
        Look up the current value of the state.
        """

        raise "Your code here."

    def getQValue(self, state, action):
        """
        Look up the current q-value of the state action pair.
        """

        raise "Your code here."

    def getPolicy(self, state):
        """
        Look up the current recommendation for the state.
        """

        raise "Your code here."

    def getAction(self, state):
        """
        Choose an action: this will require that your agent balance
        exploration and exploitation as appropriate.
        """

        raise "Your code here."

    def update(self, state, action, nextState, reward):
        """
        Update parameters in response to the observed transition.
        """

        raise "Your code here."
