import matplotlib as mpl
mpl.use('Agg')
import logging
logger = logging.getLogger(__name__)
from Algorithms.BlackBox.Bandits.EpsilonGreedy import *

class EpsilonGreedyAnnealing(EpsilonGreedy):
    def __init__(self,dimensions_definition):
        EpsilonGreedy.__init__(self,dimensions_definition=dimensions_definition)
        self.calculate_Epsilon()

    def calculate_Epsilon(self):
        eps = self.get_total_counts()
        self.epsilon = 1/(np.log(eps+0.000001))
        if self.epsilon > 1:
            self.epsilon = 1
        if self.epsilon < 0:
            self.epsilon = 0

    def get_new_trials(self, unit_diversion=[], context=[]):
        self.calculate_Epsilon()
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

