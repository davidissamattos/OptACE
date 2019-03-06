#This file handles saving and loading the Model from the database

from Database import ConnectionDB
import datetime
import os
import json
import numpy as np
import pandas as pd
import pickle
import logging
logger = logging.getLogger(__name__)

class ModelDB(object):
    def __init__(self,jobname):
        """Init
        Gets connection with the database
        """
        self.db = ConnectionDB.ConnectionDB(jobname)
        self.collection = 'models'
        self.jobname = jobname

    def get_last_model(self):
        """
        Loads from the database collection the latest model
        The model is unpickled before returning
        :return: the latest model
        """
        try:
            latest_model = self.db.get_lastest_entity(collection=self.collection)
            # Removing from vector form
            model = latest_model['model']
            return pickle.loads(model)
        except Exception as e:
            logger.exception(e)

    def save_model(self, model):
        """
        Passes a model to be saved in the database
        The model is pickled before being saved
        :param model: model to be saved
        :return:
        """
        try:
            pickled_object = pickle.dumps(model)
            log = {
                'model': pickled_object
            }
            self.db.save_one_entity(collection=self.collection, entity=log)

        except Exception as e:
            logger.exception(Exception)
            logger.exception(e)
            pass
