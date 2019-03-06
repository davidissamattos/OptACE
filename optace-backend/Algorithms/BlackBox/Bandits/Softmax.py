import matplotlib as mpl
mpl.use('Agg')
import logging
logger = logging.getLogger(__name__)
from Algorithms.BlackBox.Bandits.BasicBandit import *


class Softmax(BasicBandit):
    def __init__(self, dimensions_definition, temperature=1):
        BasicBandit.__init__(self, dimensions_definition=dimensions_definition)
        if temperature<=0:
            self.T = 1
        else:
            self.T = temperature
        self.denominator = self.calculate_denominator()

    def calculate_denominator(self):
        den_sum = []
        for index in range(self.narms):
            value = np.exp(self.get_mean_for_index(index)/self.T)
            den_sum.append(value)
        self.denominator = np.sum(den_sum)

    def calculate_probability_for_index(self,index):
        self.arm_list[index,self.DecisionCriteria] = np.exp(self.get_mean_for_index(index)/self.T)/self.denominator

    def update_all_probabilities(self):
        for index in range(self.narms):
            self.calculate_probability_for_index(index)

    def update_probability_vector(self):
        self.calculate_denominator()
        self.update_all_probabilities()

    def get_probability_vector(self):
        self.update_probability_vector()
        prob_vector = self.arm_list[:, self.DecisionCriteria]
        return prob_vector/np.sum(prob_vector)

    def get_probability_for_index(self,index):
        return self.arm_list[index][self.DecisionCriteria]

    def get_new_trials(self, unit_diversion=[], context=[]):
        prob_vector = self.get_probability_vector()
        armindex = np.random.choice(self.narms,1,p=prob_vector)[0]
        arm = self.get_arm_value_for_index(armindex)
        trial = []
        trial.append(arm)
        return trial

    def update_model(self, trial, objective, context=[]):
        chosen_arm = trial[0]
        reward = objective[0]
        index = self.get_index_for_chosen_arm(chosen_arm)
        if index == -1:
            logger.warning("no arm selected")
            return
        else:
            self.update_stats_for_index(index=index, reward=reward)
            self.update_all_ucb()
            self.update_probability_vector()
            # print self.arm_list
            return
