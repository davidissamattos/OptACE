import numpy as np
import matplotlib as mpl
import copy
mpl.use('Agg')
from Algorithms.BlackBox.BlackBox import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

import logging
logger = logging.getLogger(__name__)

class BayesianOptimization(BlackBox):
    """

    """