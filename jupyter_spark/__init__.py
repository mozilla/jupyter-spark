from notebook.utils import url_path_join

from .spark import SparkHandler


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        # the path is relative to the `jupyter_spark` directory
        'src': 'static',
        # directory in the `nbextension/` namespace
        'dest': 'jupyter-spark',
        # _also_ in the `nbextension/` namespace
        'require': 'jupyter-spark/extension',
    }]


def _jupyter_server_extension_paths():
    return [{
        'module': 'jupyter_spark',
    }]


def load_jupyter_server_extension(nbapp):
    # Extract our Spark server details from the config:
    config = nbapp.config['NotebookApp']
    host = config.get('spark_host', 'http://localhost:4040')
    prefix = config.get('spark_prefix', '/spark')

    url = nbapp.web_app.settings['base_url']
    nbapp.web_app.add_handlers(
        r'.*',  # match any host
        [
            (url_path_join(url, prefix) + '.*', SparkHandler, {
                'host': host,
                'url': url,
                'prefix': prefix,
            }),
        ]
    )
    nbapp.log.info("Jupyter-Spark enabled!")
