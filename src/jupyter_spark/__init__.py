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
    spark_url = config.get('spark_url', 'http://localhost:4040')
    spark_endpoint = config.get('spark_endpoint', '/spark')

    nbapp.web_app.add_handlers(
        r'.*',  # match any host
        [
            (spark_endpoint + '.*', SparkHandler, {
                'base_url': nbapp.web_app.settings['base_url'],
                'spark_url': spark_url,
                'spark_endpoint': spark_endpoint,
            }),
        ]
    )
    nbapp.log.info("Jupyter-Spark enabled!")
