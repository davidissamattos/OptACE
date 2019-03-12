#importing the algorithm
from Algorithms.BlackBox.ContinuousSpace.LGHOO import *
from Algorithms.BlackBox.ContinuousSpace.DOO import *
from Algorithms.BlackBox.Bandits.UCB1 import *


from Database.ConfigurationDB import ConfigurationDB
from Database.ModelDB import ModelDB
from Database.RawDataDB import RawDataDB
from Database.RequestsDB import RequestsDB
import logging
logger = logging.getLogger(__name__)


class BlackBoxCoordinator:
    def __init__(self, jobname):
        """
        Initialize the coordinator with basic information of the job
        """
        try:
            logger.info('Initialing Coordinator for the job: '+str(jobname))
            self.jobname = str(jobname)
            self.configDB = ConfigurationDB(jobname=self.jobname)
            self.configDB.get_last_config()

            self.signals_key = self.configDB.get_signals()
            self.algorithm = self.configDB.get_algorithm()


        except Exception as e:
            logger.exception('Error initializing the Coordinator')
            logger.exception(e)
            raise

    def initialize_model(self):
        """
        This function initializes the models and save them in the models DB so it can be retrieved later
        This is the trickiest part because every new algorithm needs a different initialization method
        :return:
        """
        algorithm_type = self.algorithm['type'].lower()

        model = []
        try:
            #Try to initialize the model
            if algorithm_type == 'lghoo':
                logger.info("Initializing the LGHOO model")
                v1 = float(self.algorithm['v1'])
                rho = float(self.algorithm['rho'])
                minimum_grow = float(self.algorithm['minimum_grow'])
                arms_def = self.algorithm['dimensions']
                model = LGHOO(dimensions_definition=arms_def, rho=rho, v1=v1, minimum_grow=minimum_grow)

            if algorithm_type == 'doo':
                logger.info("Initializing the DOO model")
                beta = float(self.algorithm['beta'])
                minimum_grow = float(self.algorithm['minimum_grow'])
                arms_def = self.algorithm['dimensions']
                model = DOO(dimensions_definition=arms_def, beta=beta, minimum_grow=minimum_grow)

            if algorithm_type == 'ucb1':
                logger.info("Initializing the UCB1 model")
                arms_def = self.algorithm['dimensions']
                model = UCB1(dimensions_definition=arms_def)


        except Exception as e:
            logger.exception("Could not initialize the model")
            logger.exception(e)

        try:
            modeldb = ModelDB(jobname=self.jobname)
            modeldb.save_model(model)
        except Exception as e:
            logger.exception("Could not save the model")
            logger.exception(e)

    def request_trial(self, unit_diversion, signals={}):
        """
        For black box models this function returns a dictionary of the new trial values
        :param signals: this is optional. If there is some context relevant to the algorithm
        That was described in the configuration it is placed here
        :return: a dictionary of the trials
        """
        requestsdb = RequestsDB(jobname=self.jobname)
        try:
            requestsdb.save(unit_diversion=unit_diversion, signals=signals)
        except Exception as e:
            logger.exception('Error logging the raw data')
            logger.warning(e)

        context = []
        try:
            context_keys = self.algorithm['context']
            for key in context_keys:
                context.append(signals[key])
        except Exception as e:
            context = []
            logger.warning('Error retrieving the context or no context was provided')
            logger.warning(e)


        model=[]
        try:
            logger.info('Getting the model from the DB')
            modeldb = ModelDB(jobname=self.jobname)
            model = modeldb.get_last_model()
        except Exception as e:
            logger.exception('Error retrieving the model from the database')
            logger.warning(e)

        try:
            trialsvector = model.get_new_trials(unit_diversion=unit_diversion, context=context)
            #preparing the dictionary to be returned
            dimensions = self.algorithm['dimensions']  # this is an array
            trials = {}
            i=0
            for dim in dimensions:
                dim_name = dim['name']
                trials[dim_name] = trialsvector[i]
                i=i+1

            logger.info('The requested trials are: '+ str(trials))
            return trials
        except Exception as e:
            logger.exception('Could not get new trials')
            logger.exception(e)
            return 'ERROR'


    def update_model(self,unit_diversion,signals):
        """
        This method loads the model and updates its internal statistics
        :param signals: depending on the model it can have one or more objective that is defined in the algorithm
        The value is retrieved from the signals
        :return:
        """
        modeldb = ModelDB(jobname=self.jobname)
        model = modeldb.get_last_model()
        rawdatadb = RawDataDB(jobname=self.jobname)

        try:
            rawdatadb.save_entity(signals=signals,unit_diversion=unit_diversion)
        except Exception as e:
            logger.exception('Error logging the raw data')
            logger.warning(e)


        #find the context of this play
        context=[]
        try:
            context_keys = self.algorithm['context']
            for key in context_keys:
                context.append(signals[key])
        except Exception as e:
            context = []
            logger.warning('Error retrieving the context or no context was provided')
            logger.warning(e)


        #Find the objectives
        objectives=[]
        try:
            objectives_keys = self.algorithm['objective'] #this is an array
            for key in objectives_keys:
                objectives.append(signals[key])
        except Exception as e:
            objectives = []
            logger.exception('Error getting the objective value')
            logger.warning(e)

        # Find the played trials
        dimensions = self.algorithm['dimensions']  # this is an array
        played_trial = []
        for dim in dimensions:
            dim_name = dim['name']
            played_trial.append(signals[dim_name])

        model.update_model(trial=played_trial,objective=objectives,context=context)

        #after updating we save the model
        modeldb.save_model(model)

    def get_result(self):
        modeldb = ModelDB(jobname=self.jobname)
        model = modeldb.get_last_model()
        results = model.get_results()
        dimensions = self.algorithm['dimensions']  # this is an array
        best_arm_dic = {}
        i=0
        for dim in dimensions:
            dim_name = dim['name']
            best_arm_dic[dim_name]=results[i]
            i=i+1

        return best_arm_dic

