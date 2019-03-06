import matplotlib as mpl
mpl.use('Agg')
import logging
logger = logging.getLogger(__name__)
from Algorithms.BlackBox.Bandits.BasicBandit import *


class EpsilonGreedy(BasicBandit):
    def __init__(self, dimensions_definition,epsilon=0.2):
        BasicBandit.__init__(self, dimensions_definition=dimensions_definition)
        if epsilon<0 or epsilon>1:
            self.epsilon = 0.2
        else:
            self.epsilon = epsilon


    def get_new_trials(self, unit_diversion=[], context=[]):
        choice = int(np.random.choice(2, 1, p=[self.epsilon, 1 - self.epsilon]))
        armindex = []
        if choice == 0:
            armindex = np.random.choice(self.narms, 1)[0]
        if choice == 1:
            armindex = self.get_max_mean_index()
        arm = self.get_arm_value_for_index(armindex)
        trial=[]
        trial.append(arm)
        return trial

    def update_model(self,trial,objective,context=[]):
        chosen_arm=trial[0]
        reward=objective[0]
        index =self.get_index_for_chosen_arm(chosen_arm)
        if index == -1:
            logger.warning("no arm selected")
            return
        else:
            self.update_stats_for_index(index=index, reward=reward)
            self.update_all_ucb()

            return



