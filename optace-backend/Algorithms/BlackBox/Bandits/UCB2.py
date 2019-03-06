import matplotlib as mpl
mpl.use('Agg')
import logging
logger = logging.getLogger(__name__)
from Algorithms.BlackBox.Bandits.BasicBandit import *

class UCB2(BasicBandit):
    """Based on the multi-armed bandit book by White"""
    def __init__(self, dimensions_definition,alpha):
        BasicBandit.__init__(self, dimensions_definition=dimensions_definition)
        if alpha >0 and alpha <1:
            self.alpha = alpha
        else:
            self.alpha = 0.5

        self.current_arm_index = 0
        self.next_update = 0

    def get_r_for_index(self,index):
        return self.arm_list[index][self.DecisionCriteria]

    def update_r_for_index(self, index):
        self.arm_list[index,self.DecisionCriteria] = self.arm_list[index,self.DecisionCriteria] +1

    def calculate_tau_for_index(self,index):
        ri = self.get_r_for_index(index)
        return np.power(1 + self.alpha, ri)

    def calculate_next_tau_for_index(self,index):
        ri = self.get_r_for_index(index) + 1
        return np.power(1 + self.alpha, ri)

    def set_arm_for_index(self,index):
        self.current_arm_index = index
        self.next_update = self.next_update + max(1, self.calculate_next_tau_for_index(index) - self.calculate_tau_for_index(index))
        self.update_r_for_index(index)

    def calculate_ucb_for_index(self, index):
        """
        Uses a different bound than the UCB1
        :param index:
        :return:
        """

        counts = self.get_count_for_index(index)
        if counts > 0:
            tau = self.calculate_tau_for_index(index)
            uncertainty_bound = math.sqrt((1+self.alpha)*(math.log(np.e * self.get_total_counts()/tau)) / (2*tau))
            mean = self.get_mean_for_index(index)
            ucb_value = mean + uncertainty_bound
        else:
            ucb_value = np.inf
        return ucb_value


    def select_arm_index(self):
        armindex = []
        #Making sure every arm is selected at least once
        for i in range(self.narms):
            if self.get_count_for_index(i) == 0:
                self.set_arm_for_index(i)
                self.current_arm_index = i
                #print "current arm index", self.current_arm_index
                return int(self.get_arm_value_for_index(self.current_arm_index))

        #If after we select we are still in the same epoch we keep selecting this arm
        if self.next_update > self.get_total_counts():
            #print "current arm index", self.current_arm_index
            return int(self.get_arm_value_for_index(self.current_arm_index))

        #If we are in new epoch we select
        armindex = self.get_max_bound_index()
        #print "arm index ", armindex
        self.set_arm_for_index(armindex)
        return int(armindex)

    def get_new_trials(self, unit_diversion=[], context=[]):
        armindex = int(self.select_arm_index())
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
            # print self.arm_list
            return