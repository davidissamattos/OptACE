import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from Algorithms.BlackBox.BlackBox import *

import logging
logger = logging.getLogger(__name__)


class BasicBandit(BlackBox):
    def __init__(self,dimensions_definition):
        self.ArmIndex = 0
        self.Bound = 1
        self.Counts = 2
        self.Mean = 3
        self.SumRewards = 4
        self.M2 = 5
        self.DecisionCriteria = 6


        self.initial_rvalue = 6
        self.initial_M2 = 0
        self.initial_bound = np.inf
        self.initial_mean = 0
        self.initial_counts = 0
        self.inital_sumrewards = 0
        self.initial_DecisionCriteria = 0

        self.arm_list = np.array([np.zeros(7)])
        self.arm_list[0, self.ArmIndex] = 0
        self.arm_list[0, self.Bound] = self.initial_bound
        self.arm_list[0, self.Counts] = self.initial_counts
        self.arm_list[0, self.Mean] = self.initial_mean
        self.arm_list[0, self.SumRewards] = self.inital_sumrewards
        self.arm_list[0, self.M2] = self.initial_M2
        self.arm_list[0, self.DecisionCriteria] = self.initial_DecisionCriteria

        #Basic bandits has only one dimension
        self.arms_def = dimensions_definition[0]
        self.arm_values = self.arms_def['values']
        self.narms = len(self.arm_values)

        initarray = np.zeros(6)
        initarray[self.ArmIndex]=0
        initarray[self.Bound] = self.initial_bound
        initarray[self.Counts] = self.initial_counts
        initarray[self.Mean] = self.initial_mean
        initarray[self.SumRewards] = self.inital_sumrewards
        initarray[self.M2] = self.initial_M2
        self.arm_list = np.stack(initarray)

        for i in range(1, self.narms):
            initarray[self.ArmIndex] = i
            self.arm_list = np.vstack((self.arm_list, initarray))

    #Some helper functions

    def get_index_for_chosen_arm(self,chosen_arm):
        try:
            index= self.arm_values.index(chosen_arm)
        except Exception as e:
            index = -1
        return int(index)

    def get_bound_for_index(self, index):
        return self.arm_list[index, self.Bound]

    def set_bound_for_index(self, index, bound):
        self.arm_list[index, self.Bound] = bound

    def get_max_bound(self):
        return np.max(self.arm_list[:,self.Bound])

    def get_max_bound_index(self):
        maxbound = self.get_max_bound()
        maxlist = self.arm_list[self.arm_list[:,self.Bound]==maxbound]
        index = maxlist[np.random.choice(len(maxlist.tolist()),1)[0],self.ArmIndex]
        return int(index)

    def update_all_ucb(self):
        narms = self.narms
        for i in range(narms):
            self.set_bound_for_index(index=i,bound=self.calculate_ucb_for_index(i))


    def calculate_ucb_for_index(self, index):
        """
        Calculate the ucb estimate for an element
        :param index:
        :return:
        """
        counts = self.get_count_for_index(index)
        if counts > 0:
            uncertainty_bound = math.sqrt((2 * math.log(self.get_total_counts())) / float(self.get_count_for_index(index)))
            mean = self.get_mean_for_index(index)
            ucb_value = mean + uncertainty_bound
        else:
            ucb_value = np.inf
        return ucb_value

    def get_count_for_index(self, index):
        return self.arm_list[index][self.Counts]

    def update_n_count_for_index(self, index, n):
        self.arm_list[index][2] = self.arm_list[index][self.Counts] + n

    def update_count_for_index(self, index):
        self.update_n_count_for_index(index, 1)

    def get_reward_for_index(self, index):
        return self.arm_list[index][self.SumRewards]

    def update_reward_for_index(self, index, sum_rewards):
        self.arm_list[index,self.SumRewards] = self.arm_list[index, self.SumRewards] + sum_rewards

    def get_mean_for_index(self, index):
        return self.arm_list[index, self.Mean]

    def get_all_index_max_mean(self):
        """
        Return an array with the index of all max bounds if there is more than one
        :return:
        """
        return np.argwhere(self.arm_list[:, self.Mean] == np.amax(self.arm_list[:, self.Mean]))

    def get_max_mean_index(self):
        return self.get_all_index_max_mean()[0][0]

    def update_n_mean_for_index(self, index, n, sum_new_rewards):
        """
        Update the mean and the counts for the played arm
        :param index:
        :param n:
        :param sum_new_rewards:
        :return:
        """
        self.update_reward_for_index(index, sum_new_rewards)

        n_old = self.get_count_for_index(index)
        # update the count for the played arm
        self.update_n_count_for_index(index, n)
        n_new = self.get_count_for_index(index)

        old_mean = self.get_mean_for_index(index)

        new_mean = (old_mean * n_old + sum_new_rewards) / float(n_new)
        self.arm_list[index][self.Mean] = new_mean

    def update_mean_for_index(self, index, reward):
        self.update_n_mean_for_index(index=index, n=1, sum_new_rewards=reward)

    def update_stats_for_index(self,index,reward):
        self.update_M2_for_index(index=index,reward=reward)
        self.update_mean_for_index(index=index,reward=reward)

    # updating the standard deviation iteratively
    def update_M2_for_index(self, index, reward):
        #this is should be called before we update the mean
        #https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
        count = self.get_count_for_index(index) + 1
        mean = self.get_mean_for_index(index)
        delta = reward - mean
        mean = mean + delta / count
        delta2 = reward-mean
        M2 = self.get_M2_for_index(index)
        newM2 = M2 + delta*delta2
        self.arm_list[index][self.M2] = newM2

    def get_M2_for_index(self,index):
        return self.arm_list[index][self.M2]

    def get_variance_for_index(self, index):
        count = self.get_count_for_index(index)
        M2 = self.get_M2_for_index(index)
        if count < 2:
            return np.nan
        else:
            return M2/(count-1)

    def get_total_counts(self):
        return np.sum(self.arm_list[:, self.Counts])

    def get_arm_value_for_index(self,index):
        arm = self.arm_values[index]
        return arm

    def get_results(self):
        maxmeanindex = self.get_max_mean_index()
        return self.get_arm_value_for_index(maxmeanindex)
