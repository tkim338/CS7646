""""""  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		     		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		     		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		     		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		     		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		     		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		     		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		     		  		  		    	 		 		   		 		  
or edited.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		     		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		     		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		     		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Student Name: Thomas Kim (replace with your name)  		  	   		     		  		  		    	 		 		   		 		  
GT User ID: tkim338 (replace with your User ID)  		  	   		     		  		  		    	 		 		   		 		  
GT ID: 902871961 (replace with your GT ID)  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import random as rand  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import numpy as np  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
class QLearner(object):  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    This is a Q learner object.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    :param num_states: The number of states to consider.  		  	   		     		  		  		    	 		 		   		 		  
    :type num_states: int  		  	   		     		  		  		    	 		 		   		 		  
    :param num_actions: The number of actions available..  		  	   		     		  		  		    	 		 		   		 		  
    :type num_actions: int  		  	   		     		  		  		    	 		 		   		 		  
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		     		  		  		    	 		 		   		 		  
    :type alpha: float  		  	   		     		  		  		    	 		 		   		 		  
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		     		  		  		    	 		 		   		 		  
    :type gamma: float  		  	   		     		  		  		    	 		 		   		 		  
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		     		  		  		    	 		 		   		 		  
    :type rar: float  		  	   		     		  		  		    	 		 		   		 		  
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		     		  		  		    	 		 		   		 		  
    :type radr: float  		  	   		     		  		  		    	 		 		   		 		  
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		     		  		  		    	 		 		   		 		  
    :type dyna: int  		  	   		     		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		     		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        num_states=100,  		  	   		     		  		  		    	 		 		   		 		  
        num_actions=4,  		  	   		     		  		  		    	 		 		   		 		  
        alpha=0.2,  		  	   		     		  		  		    	 		 		   		 		  
        gamma=0.9,  		  	   		     		  		  		    	 		 		   		 		  
        rar=0.5,  		  	   		     		  		  		    	 		 		   		 		  
        radr=0.99,  		  	   		     		  		  		    	 		 		   		 		  
        dyna=0,  		  	   		     		  		  		    	 		 		   		 		  
        verbose=False,  		  	   		     		  		  		    	 		 		   		 		  
    ):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		     		  		  		    	 		 		   		 		  
        self.num_actions = num_actions
        self.num_states = num_states
        self.s = 0  		  	   		     		  		  		    	 		 		   		 		  
        self.a = 0

        self.Q = np.zeros((num_states, num_actions)) # [[0] * num_states] * num_actions
        self.rar = rar
        self.radr = radr
        self.alpha = alpha * 2
        self.gamma = gamma
        self.dyna = dyna

        self.T = np.zeros((num_states, num_actions, num_states)) + 0.00001 # [[[0.000001] * num_states] * num_actions] * num_states
        self.R = np.zeros((num_states, num_actions)) # [[0] * num_states] * num_actions

    def choose_action(self, s_prime):
        a_prime = self.optimal_action(s_prime)

        if np.random.random() < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = a_prime

        self.rar *= self.radr

        return action # , a_prime

    def optimal_action(self, s):
        # max_actions = []
        # for i in range(len(self.Q[s])):
        #     if self.Q[s][i] == np.max(self.Q[s], axis=1):
        #         max_actions.append(i)
        # a_prime = np.random.choice(max_actions)
        a_prime = np.argmax(self.Q[s], axis=1)
        return a_prime

    def update_Q(self, s, a, r, s_prime, a_prime):
        r = np.array(r)
        s_prime = np.array(s_prime)
        self.Q[s_prime[r == 1]] = 1

        self.Q[s, a] = (1 - self.alpha) * self.Q[s, a] + self.alpha * (r + self.gamma * self.Q[s_prime, a_prime])

    def update_T(self, s, a, s_prime):
        self.T[s, a, s_prime] += 1

    def update_R(self, s, a, r):
        s = np.array(s)
        r = np.array(r)
        self.R[s, a] = (1 - self.alpha) * self.R[s, a] + self.alpha * r
        self.R[s[r == 1]] = 1

    def querysetstate(self, s):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Update the state without updating the Q-table  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        :param s: The new state  		  	   		     		  		  		    	 		 		   		 		  
        :type s: int  		  	   		     		  		  		    	 		 		   		 		  
        :return: The selected action  		  	   		     		  		  		    	 		 		   		 		  
        :rtype: int  		  	   		     		  		  		    	 		 		   		 		  
        """
        action = self.choose_action([s])
        # self.s = s
        # action = rand.randint(0, self.num_actions - 1)
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

            dyna_s = np.random.randint(0, self.num_states, self.dyna * 10)
            dyna_a = np.random.randint(0, self.num_actions, self.dyna * 10)
            dyna_s_prime = np.argmax(self.T[dyna_s, dyna_a], axis=1)
            dyna_r = self.R[dyna_s_prime, dyna_a]
            self.update_Q(dyna_s, dyna_a, dyna_r, dyna_s_prime, self.optimal_action(dyna_s_prime))

        self.s = s_prime
        self.a = action

        return action

    def author(self):
        return 'tkim338'
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("Remember Q from Star Trek? Well, this isn't him")