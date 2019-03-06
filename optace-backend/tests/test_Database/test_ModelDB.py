import unittest
from main import app
import json
import os
from pymongo import MongoClient

from Database.ModelDB import *

# class test_ACEAlgoDB(unittest.TestCase):
#
#     def setUp(self):
#         # dblocation = os.environ['MONGODB']
#         # self.client = MongoClient(dblocation)
#         # self.configdb = ACEConfigurationDB(experiment_name)
#         # try:
#         #     self.client.drop_database(experiment_name)
#         # except:
#         #     pass
#         # unit_diversion = config['unit_diversion']
#         # factors = config['factors']
#         # factor0 = factors[0]
#         # algorithm = factor0['algorithm']
#         # algorithm_type = algorithm['type']
#         # metrics = config['metrics']
#         # signals = config['signals']
#         # self.configdb.log(data=config)
#         # self.configdb.get_LastUpdate()
#         # self.algodb = ACEAlgoDB(experiment_name, collection=collection)
#
#
#     def tearDown(self):
#         # self.client.drop_database(experiment_name)
#         # self.client.close()
#
#     def test_all(self):
#         # self.algodb.log(fakeobject)
#         # unpickled_fakeobject = self.algodb.get_Last()
#         # #comparing the pickled version instead of the array
#         # self.assertEqual(pickle.dumps(unpickled_fakeobject), pickle.dumps(fakeobject))