from Database import ConnectionDB

import datetime
import os
import json
import numpy as np
import pandas as pd
import pickle
import logging
logger = logging.getLogger(__name__)

class ConfigurationDB():
    def __init__(self,jobname):
        """Init
        Gets connection with the database
        """
        self.db = ConnectionDB.ConnectionDB(jobname)
        self.collection = 'configuration'
        self.jobname = jobname

    # Configuration of the experiment
    def save_job_configuration(self, configuration_data):
        """Save the configuration parameters for a job in the mongoDB"""
        unit_diversion = json.dumps(configuration_data['unit_diversion']) #string
        algorithm = configuration_data['algorithm'] #dictionary
        signals = configuration_data['signals']

        try:
            config_version = self.db.get_number_of_entities(self.collection)
        except Exception as e:
            logger.exception(e)
            config_version = 1

        config = {
            'job': self.jobname,
            'unit_diversion': unit_diversion,
            'algorithm': algorithm,
            'signals': signals,
            'config_version': config_version,
        }

        self.db.save_one_entity(collection=self.collection, entity=config)

    def get_last_config(self):
        """Get the configuration parameters from the database"""
        try:
            # Setting up the query
            config = self.db.get_lastest_entity(collection=self.collection)
            self.config = config
            self.config.pop('_id') #removing the _id so it can be put in a json form

            self.jobname = config['job']
            self.algorithm= config['algorithm']
            self.unit_diversion = config['unit_diversion']
            self.signals = config['signals']

            return config

        except Exception as e:
            logger.warning('Could not get last configuration')
            logger.exception(e)

    def get_configuration_version(self):
        """
        Get the current configuration version
        :return: config version
        """
        try:
            self.get_last_config()
            version = self.config['config_version']
        except Exception as e:
            logger.exception(e)
            version=1
        return version

    def get_timestamp(self):
        """
        Get the timestamp of the last config variation
        :return: timestamp
        """
        self.get_last_config()
        return self.config['timestamp']

    def get_jobname(self):
        """
        Get the name of the job
        :return: jobname
        """
        self.get_last_config()
        return self.jobname

    def get_unit_diversion(self):
        """
        Get the name of the unit of diversion
        :return: unit_diversion
        """
        self.get_last_config()
        return self.unit_diversion

    def get_signals(self):
        """
        Get the signals keys
        :return: signals
        """
        self.get_last_config()
        return self.signals

    def get_algorithm(self):
        """Get the unit of diversion name"""
        self.get_last_config()
        return self.algorithm
