from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from nbconvert.exporters.export import *
import requests
import tornado
import os
import logging

# Example usage: tornado_logger.error("This is an error!")
tornado_logger = logging.getLogger("tornado.application")

def raise_error(msg):
    raise tornado.web.HTTPError(500, "ERROR: " + msg)

class SparkHandler(IPythonHandler):
    def get(self):
        print("I'm running the extension. Whooooooo!!!")

def load_jupyter_server_extension(nb_server_app):
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/spark')
    web_app.add_handlers(host_pattern, [(route_pattern, SparkHandler)])
