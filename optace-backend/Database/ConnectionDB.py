import pymongo
from pymongo import MongoClient
import datetime
import os
import logging
logger = logging.getLogger(__name__)

class ConnectionDB():
    def __init__(self, database_name):
        """Init
        Each experiment/job is a new Mongo db
        """
        self.dbclient = self.get_client()
        self.database_name = database_name
        self.db = self.dbclient[database_name]

    def get_client(self):
        dblocation = os.environ['MONGODB']
        return MongoClient(dblocation)


    def save_one_entity(self, collection, entity):
        try:
            entity['timestamp'] = datetime.datetime.utcnow()
            self.db[collection].insert_one(entity)
        except Exception as e:
            logger.exception('Could not save in the database')
            logger.exception(e)

    def get_all_entities(self, collection):
        try:
            # Setting up the query
            entities = list(self.db[collection].find().sort('timestamp', pymongo.DESCENDING))
            return entities
        except Exception as e:
            logger.exception(e)

    def get_n_latest_entities(self, collection, n):
        try:
            # Setting up the query
            entities = list(self.db[collection].find().sort('timestamp', pymongo.DESCENDING).limit(int(n)))
            return entities
        except Exception as e:
            logger.exception(e)

    def get_lastest_entity(self, collection):
        try:
            # Setting up the query
            entity = self.db[collection].find().sort('timestamp', pymongo.DESCENDING)[0]
            return entity
        except Exception as e:
            logger.exception(e)

    # def get_last_logged_entity_by_keyValue(self, collection, key, value):
    #     try:
    #         # Setting up the query
    #         entity = self.db[collection].find({key: value}).sort('timestamp', pymongo.DESCENDING)[0]
    #         return entity.pop('_id')
    #     except Exception as e:
    #         logger.exception(e)

    def get_number_of_entities(self, collection):
        try:
            # Setting up the query
            return self.db[collection].find({}).count()
        except Exception as e:
            logger.exception(e)

    def close_connections(self):
        self.dbclient.close()