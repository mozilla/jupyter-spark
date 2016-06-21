from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import requests
import tornado
import os
import logging
import json
from bs4 import BeautifulSoup

EXTENSION_URL = "/spark"

# Example usage: tornado_logger.error("This is an error!")
tornado_logger = logging.getLogger("tornado.application")


def raise_error(msg):
    raise tornado.web.HTTPError(500, "ERROR: " + msg)


class SparkHandler(IPythonHandler):
    spark_host = None
    web_app = None

    def get(self):
        if not self.request.uri.startswith(EXTENSION_URL):
            raise_error("URI did not start with " + EXTENSION_URL)
        spark_request = self.spark_host + self.request.uri[len(EXTENSION_URL):]

        try:
            spark_response = requests.get(spark_request)

            content_type = spark_response.headers['content-type']
            self.set_header("Content-Type", content_type)

            if "text" in content_type:
                # Replace all the relative links with our proxy links
                soup = BeautifulSoup(spark_response.text, "html.parser")

                for has_href in ['a', 'link']:
                    for a in soup.find_all(has_href):
                        if "href" in a.attrs:
                            a['href'] = url_path_join(self.web_app, a['href'])

                for has_src in ['img', 'script']:
                    for a in soup.find_all(has_src):
                        if "src" in a.attrs:
                            a['src'] = url_path_join(self.web_app, a['src'])

                client_response = str(soup)
            else:
                # Probably binary response, send it directly.
                client_response = spark_response.content

        except requests.exceptions.RequestException:
            client_response = json.dumps({"error": "SPARK_NOT_RUNNING"})

        self.write(client_response)
        self.flush()


def load_jupyter_server_extension(nb_server_app):
    # Extract our Spark server details from the config:
    cfg = nb_server_app.config["NotebookApp"]
    SparkHandler.spark_host = cfg.get("spark_host", "http://localhost:4040")

    web_app = nb_server_app.web_app
    host_pattern = ".*$"
    route_pattern = url_path_join(
        web_app.settings['base_url'], EXTENSION_URL) + ".*"
    web_app.add_handlers(host_pattern, [(route_pattern, SparkHandler)])

    SparkHandler.web_app = url_path_join(
        web_app.settings['base_url'], EXTENSION_URL)
