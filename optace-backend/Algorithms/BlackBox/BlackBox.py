from abc import ABC, abstractmethod


class BlackBox(ABC):

    @abstractmethod
    def update_model(self,trial,objective,context):
        """
        Updates the internal state of the model based on the received data
        All the input data are lists in the same order as the lists in the configuration file
        :param trial: this represents the tried values that we are modifying in each dimension
        :param objective: a list with the multiple objectives. Most algorithms are single objective
        In this case instantiate this class as objective[0]
        :param context: this is the context if necessary
        :return:
        """
        print("update_model")

    @abstractmethod
    def get_new_trials(self, unit_diversion, context):
        """
        Gets the next set of trials to be tested
        :param unit_diversion: if want to keep consistency...
        :param context: if using an algorithm that uses context
        :return: a list with the new values in the dimensions
        """
        print("get_new_trials")

    @abstractmethod
    def get_results(self):
        """
        Gets the best values so far
        :param unit_diversion: if want to keep consistency...
        :param context: if using an algorithm that uses context
        :return: a list with the new values in the dimensions
        """
        print("get_results")