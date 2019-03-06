import matplotlib as mpl
mpl.use('Agg')
import logging
logger = logging.getLogger(__name__)
from Algorithms.BlackBox.Bandits.BasicBandit import *

class UCB1(BasicBandit):
    def __init__(self, dimensions_definition):
        BasicBandit.__init__(self, dimensions_definition=dimensions_definition)

    def get_new_trials(self, unit_diversion=[], context=[]):
        index = self.get_max_bound_index()
        arm = self.get_arm_value_for_index(index)
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
            #print self.arm_list
            return



