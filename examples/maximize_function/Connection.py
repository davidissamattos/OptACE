import requests
import logging
logger = logging.getLogger(__name__)

#Server configurations and URL
requestURL = "/blackbox/request_trial"
bestArmURL = "/blackbox/get_best_arm"
logURL = "/blackbox/update_model"


class Connection(object):
    """
    This class establish the connection with the server.
    Configuration, clearing and visualization are NOT done here
    """
    def __init__(self, server_url="http://127.0.0.1", port=5000):
        server = server_url+":"+str(int(port))+"/api"
        self.RequestURL = server + requestURL
        self.LogURL = server + logURL
        self.bestArmURL = server + bestArmURL

    def log(self,data):
        r = requests.post(self.LogURL, json=data)
        if r.status_code == 200:
            pass
            #print "Log succeeded"
        else:
            print("Log failed")

    def request(self,data):
        r = requests.post(self.RequestURL, json=data)
        if r.status_code == 200:
            #print "json ", r.json()
            return r.json()
        else:
            raise Exception
            #return "error"

    def best_arm(self, data):
        r = requests.post(self.bestArmURL, json=data)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception
            #return "error"
