import os
import logging
import ast
import json

from Coordinator.BlackBoxCoordinator import BlackBoxCoordinator
from Database.ConfigurationDB import ConfigurationDB


#Flask
from flask import Flask, send_file, make_response
from flask import render_template
from flask import request  # for processing requests in the URL
from flask import abort
import uuid

from werkzeug.contrib.fixers import ProxyFix


try:
    level=str(os.environ['LOGGER_LEVEL'])
except:
    level='warning'
if level.lower()=='debug':
    logging.basicConfig(level=logging.DEBUG)
if level.lower()=='info':
    logging.basicConfig(level=logging.INFO)
if level.lower() == 'warning':
    logging.basicConfig(level=logging.WARNING)
if level.lower() == 'critical':
    logging.basicConfig(level=logging.CRITICAL)
else:
    logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)



app = Flask(__name__)
#Making Flask work with Werzeug
logger.info("Using database located at: " + str(os.environ['MONGODB']))
app.wsgi_app = ProxyFix(app.wsgi_app)



###### BlackBox requests
@app.route("/api/blackbox/request_trial", methods=['POST'])
def api_bb_request_trial():
    """
    This request is passed to the coordinator to handle requests for new trials in the blackbox model
    :return:
    """
    logging.info("api/blackbox/request_trial called")
    try:
        data = request.get_json()
        jobname = str(data['job'])
        try:
            unit_diversion = str(data['unit_diversion'])
        except Exception as e:
            unit_diversion = str(uuid.uuid4())
            logging.warning('No unit of diversion provided')
        try:
            signals = data['signals']
        except Exception as e:
            signals = {}
            logging.warning('No signals were provided for the request trial')
        #Here is when we actually call the experimentation framework
        coord = BlackBoxCoordinator(jobname=jobname)
        trials = coord.request_trial(unit_diversion=unit_diversion, signals=signals)
        #The json string is then sent back
        reply_data = json.dumps(trials)
        return reply_data
    except Exception as e:
        logging.exception(e)
        logging.warning("Error requesting experiment variation")
        abort(404)


@app.route("/api/blackbox/update_model", methods=['POST'])
def api_bb_update_model():
    """
    This API is for logging experiment config.
    We receive the experiment name and we log n ndb the json file
    """
    logging.info("/api/blackbox/update_model called")
    try:
        data = request.get_json()
        jobname = str(data['job'])

        try:
            unit_diversion = str(data['unit_diversion'])
        except Exception as e:
            unit_diversion = str(uuid.uuid4())
            logging.warning('No unit of diversion provided')

        try:
            signals = data['signals']
        except Exception as e:
            signals = {}
            logging.warning('No signals were provided for the request trial')

        coord = BlackBoxCoordinator(jobname=jobname)
        coord.update_model(unit_diversion=unit_diversion, signals=signals)

        return "OK"
    except Exception as e:
        logging.exception(e)
        abort(404)

@app.route("/api/blackbox/configure_job", methods=['POST'])
def configure_job():
    """
    API to configure the job through a JSON post and clear the initialize the model
    """
    logging.info("/api/blackbox/configure_job called")
    try:
        data = request.get_json()
        jobname = str(data['job'])
        configdb = ConfigurationDB(jobname=jobname)
        configdb.save_job_configuration(configuration_data=data)
        coord = BlackBoxCoordinator(jobname=jobname)
        coord.initialize_model()
        return "OK"
    except Exception as e:
        logging.exception(e)
        abort(404)

@app.route("/api/blackbox/get_best_arm", methods=['POST'])
def get_best_arm():
    """
    API to configure the job through a JSON post and clear the initialize the model
    """
    logging.info("/api/blackbox/get_best_arm called")
    try:
        data = request.get_json()
        jobname = str(data['job'])
        coord = BlackBoxCoordinator(jobname=jobname)
        return json.dumps(coord.get_result())
    except Exception as e:
        logging.exception(e)
        abort(404)

###### White box requests



###### General requests

@app.route("/api/ping/<name>", methods=['GET'])
def ping(name):
    reply = "OptACE: I am here! Ping: " +name
    return reply



###### Frontend requests




# @app.route("/api/rawdata_info", methods=['POST'])
# def frontend_getRawDataInfo():
#     """This function renders a basic html page with the expereriment_overview.html template showing an overview of the
#      experiment so far. Shows the experiment name, last configuration file, and the logged parameters"""
#     try:
#         data = request.get_json()
#         experiment_name = str(data['experiment_name'])
#         db = ACERawDataDB(experiment_name=experiment_name)
#         db.get_rawdata()
#         info = db.get_rawdata_info()
#         print info
#         return json.dumps(info, indent=4, sort_keys=True, default=jsonconverter)
#     except Exception as e:
#         logging.exception(e)
#         abort(404)





if __name__ == '__main__':
    app.run("127.0.0.1", port=5000, debug=True)