from Database import ConnectionDB
from Database import ConfigurationDB
import datetime
import os
import json
import numpy as np
import pandas as pd
import pickle
import logging
logger = logging.getLogger(__name__)

class RequestsDB(object):
    def __init__(self,jobname):
        """Init"""
        self.db = ConnectionDB.ConnectionDB(jobname)
        self.collection = 'request'
        self.jobname = jobname
        self.configDB = ConfigurationDB.ConfigurationDB(self.jobname)
        self.configDB.get_last_config()

        self.unit_diversion_key = self.configDB.get_unit_diversion()


    def save(self,unit_diversion,signals):
        """
        Save every request made
        Useful if we need to keep consistency
        :param unit_diversion:
        :param signals:
        :return:
        """
        try:
            log = {}
            log[self.unit_diversion_key] = unit_diversion
            if signals != []:
                for key, value in signals.items():
                    log[key] = value
            self.db.save_one_entity(collection=self.collection, entity=log)
            logger.info("User request saved")
        except Exception as e:
            logger.warning("Error saving the requests in the requests collection")
            logger.warning(e)

    # def get_LastVariationForKeyByUnitDiversion(self, unitdiversion, variation_key):
    #     #Do not put it in a try except otherwise it wont be catch in the ACEExperiment part
    #     logger.info("Trying to get the last variation used")
    #     object_last_query = self.db.get_last_logged_entity_by_keyValue(collection=self.collection,key=self.unit_diversion_key,value=unitdiversion)
    #     # Removing from vector form
    #     variation = object_last_query['variation'][variation_key]
    #     logger.info("Variation: " + str(variation))
    #     return variation