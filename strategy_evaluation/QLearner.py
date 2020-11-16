import random as rand
import numpy as np

class QLearner(object):
    def author(self):
        return 'tkim338'

    def __init__(
        self,
        num_states=100,
        num_actions=4,
        alpha=0.2,
        gamma=0.9,
        rar=0.5,
        radr=0.99,
        dyna=0,
        verbose=False
    ):	  	   		     		  		  		    	 		 		   		 		  
        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.s = 0
        self.a = 0

        self.Q = np.zeros((num_states, num_actions))
        self.rar = rar
        self.radr = radr
        self.alpha = alpha
        self.gamma = gamma
        self.dyna = dyna

        self.T = np.zeros((num_states, num_actions, num_states)) + 0.00001
        self.R = np.zeros((num_states, num_actions))

    def choose_action(self, s_prime):
        a_prime = self.optimal_action(s_prime)

        if np.random.random() < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = a_prime

        self.rar *= self.radr

        return action

    def optimal_action(self, s):
        a_prime = np.argmax(self.Q[s], axis=1)
        return a_prime

    def update_Q(self, s, a, r, s_prime, a_prime):
        r = np.array(r)
        # s_prime = np.array(s_prime)
        # self.Q[s_prime[r == 1]] = 1

        self.Q[s, a] = (1 - self.alpha) * self.Q[s, a] + self.alpha * (r + self.gamma * self.Q[s_prime, a_prime])

    def update_T(self, s, a, s_prime):
        self.T[s, a, s_prime] += 1

    def update_R(self, s, a, r):
        # s = np.array(s)
        r = np.array(r)
        self.R[s, a] = (1 - self.alpha) * self.R[s, a] + self.alpha * r
        # self.R[s[r == 1]] = 1

    def querysetstate(self, s):
        """
        Update the state without updating the Q-table

        :param s: The new state
        :type s: int
        :return: The selected action
        :rtype: int
        """
        action = self.choose_action([s])
        if self.verbose:
            print(f"s = {s}, a = {action}")
        return action

    def query(self, s_prime, r):
        """
        Update the Q table and return an action

        :param s_prime: The new state
        :type s_prime: int
        :param r: The immediate reward
        :type r: float
        :return: The selected action
        :rtype: int
        """
        action = self.choose_action([s_prime])

        self.update_Q([self.s], [self.a], [r], [s_prime], [action])

        if self.verbose:
            print(f"s = {s_prime}, a = {action}, r={r}")

        if self.dyna > 0:
            self.update_T([self.s], [self.a], [s_prime])
            self.update_R([s_prime], [self.a], [r])

            dyna_s = np.random.randint(0, self.num_states, self.dyna)
            dyna_a = np.random.randint(0, self.num_actions, self.dyna)
            dyna_s_prime = np.argmax(self.T[dyna_s, dyna_a], axis=1)
            dyna_r = self.R[dyna_s_prime, dyna_a]
            self.update_Q(dyna_s, dyna_a, dyna_r, dyna_s_prime, self.optimal_action(dyna_s_prime))

        self.s = s_prime
        self.a = action

        return action
