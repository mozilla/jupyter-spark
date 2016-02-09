import os
from setuptools import setup
from setuptools.command.install import install

EXT_DIR = os.path.join(os.path.dirname(__file__), 'jupyter-spark')

class InstallCommand(install):
    def run(self):
        # Import inside run() so if the user doesn't have jupyter notebook yet, we grab that dependency,
        # then run this code which imports it.
        from notebook.nbextensions import install_nbextension
        from notebook.services.config import ConfigManager
        from jupyter_core.paths import jupyter_config_dir

        # Install Python package
        install.run(self)

        # Install JavaScript extension
        install_nbextension(os.path.join(EXT_DIR, "extensions", "test.js"), overwrite=True, user=True)

        # Activate the JS extensions on the notebook
        js_cm = ConfigManager()
        js_cm.update('notebook', {"load_extensions": {'test': True}})

        # Activate the Python server extension
        server_cm = ConfigManager(config_dir=jupyter_config_dir())
        cfg = server_cm.get('jupyter_notebook_config')
        server_extensions = cfg.setdefault('NotebookApp', {}).setdefault('server_extensions', [])
        if "jupyter-spark.spark" not in server_extensions:
            cfg['NotebookApp']['server_extensions'] += ['jupyter-spark.spark']
            server_cm.update('jupyter_notebook_config', cfg)

setup(
    name="jupyter-spark",
    version="0.1.0",
    description="Jupyter Notebook extension for Apache Spark integration",
    packages=["jupyter-spark"],
    package_data={'': ['extensions/test.js']},
    install_requires = ["ipython >= 4", "jupyter-pip", "jupyter", "requests"],
    url="https://github.com/mreid-moz/jupyter-spark",
    cmdclass = {"install": InstallCommand}
)
