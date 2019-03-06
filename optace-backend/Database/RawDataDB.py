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



class RawDataDB(object):
    def __init__(self,jobname):
        """
        Gets connection with the db in the proper collection
        :param jobname:
        """
        self.db = ConnectionDB.ConnectionDB(jobname)
        self.collection = 'rawdata'
        self.jobname = jobname
        self.configDB = ConfigurationDB.ConfigurationDB(self.jobname)
        self.configDB.get_last_config()
        self.unit_diversion_key = self.configDB.get_unit_diversion()


    def save_entity(self, signals,unit_diversion):
        try:
            log = {}
            log[self.unit_diversion_key] = unit_diversion
            for key, value in signals.items():
                log[key] = value
            self.db.save_one_entity(collection=self.collection, entity=log)
        except Exception as e:
            logger.warning("Error saving entity in rawdata")
            logger.warning(e)



    def get_rawdata(self, get_all=True, number_data=10):
        """This function retrieves all the config (metrics and variations) from the database the logged experiment using the experiment name as a filter"""
        #making sure we have the experiment setup
        try:
            self.rawdata = []
            # Removing from vector form
            if get_all == True:
                #print "getting all exp config"
                entities = self.db.get_all_entities(collection=self.collection)
            else:
                #"getting limited exp config"
                entities = self.db.get_n_latest_entities(collection=self.collection, n=number_data)

            self.rawdata = entities


            #converting the entities to a pandas dataframe

            #Intitializing an empty data frame
            df = {}
            df['timestamp'] = []
            for signals_key in self.configDB.get_signals():
                df[str(signals_key)] = []
            #print "vectors initialized"

            #storing the logged config in arrays in the same order
            for entity in self.rawdata:
                df['timestamp'].append(entity['timestamp'])
                #storing the signals
                for signals_key in self.configDB.get_signals():
                    df[str(signals_key)].append(entity[str(signals_key)])

            self.rawdata_df = pd.DataFrame(df)


        except Exception as e:
            logger.exception(e)

    def get_number_retrieved_data(self):
        """return the size of the vector retrieved from the database"""
        return len(self.rawdata_df)

    def get_timestamps(self):
        """This function returns only the timestamps logged in the database"""
        return self.rawdata_df['timestamp']

    def get_retrieved_signals(self):
        """This function returns only the signals logged in the database"""
        logged_signals = {}
        for signals_key in self.configDB.get_signals():
            logged_signals[str(signals_key)] = self.rawdata_df[str(signals_key)]
            logged_signals = pd.DataFrame(logged_signals)
        return logged_signals


    def get_retrieved_dataframe(self):
        return self.rawdata_df

    def get_csv(self):
        try:
            csv = self.rawdata_df.to_csv(index=False)
            return csv
        except Exception as e:
            logger.exception(e)

    def get_html(self):
        return self.rawdata_df.to_html()

    def get_json(self):
        return json.loads(self.rawdata_df.to_json(orient='records'))

    def get_rawdata_info(self):
        dic = {}
        nrow, ncol = self.get_retrieved_dataframe().shape
        dic.update({'nrow': nrow,
                    'ncol': ncol,
                    'sample': self.get_json()})
        return dic
