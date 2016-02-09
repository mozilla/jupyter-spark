from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from nbconvert.exporters.export import *
import requests
import tornado
import os
import logging

EXTENSION_URL = "/spark"

# Example usage: tornado_logger.error("This is an error!")
tornado_logger = logging.getLogger("tornado.application")

def raise_error(msg):
    raise tornado.web.HTTPError(500, "ERROR: " + msg)

class SparkHandler(IPythonHandler):
    def get(self):
        tornado_logger.info("Received URI from client: " + self.request.uri)
        if not self.request.uri.startswith(EXTENSION_URL):
            raise_error("URI did not start with " + EXTENSION_URL)
        spark_request = "http://localhost:4040" + self.request.uri[len(EXTENSION_URL):]

        tornado_logger.info("Sending request to Spark UI: " + spark_request)
        spark_response = requests.get(spark_request)
        spark_response_json = spark_response.json()
        print(spark_response_json)

def load_jupyter_server_extension(nb_server_app):
    web_app = nb_server_app.web_app
    host_pattern = ".*$"
    route_pattern = url_path_join(web_app.settings['base_url'], EXTENSION_URL) + ".*"
    web_app.add_handlers(host_pattern, [(route_pattern, SparkHandler)])
