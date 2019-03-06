import matplotlib as mpl
mpl.use('Agg')
import logging
logger = logging.getLogger(__name__)

from Algorithms.BlackBox.Bandits.Softmax import *

class SoftmaxAnnealing(Softmax):
    def __init__(self, dimensions_definition):
        Softmax.__init__(self, dimensions_definition=dimensions_definition)

    def calculate_T(self):
        t = self.get_total_counts()
        self.T = 1/(np.log(t+0.000001))

    def calculate_denominator(self):
        den_sum = []
        self.calculate_T()
        for index in range(self.narms):
            value = np.exp(self.get_mean_for_index(index)/self.T)
            den_sum.append(value)
        self.denominator = np.sum(den_sum)


