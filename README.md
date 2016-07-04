# jupyter-spark

[![Build Status](https://travis-ci.org/mozilla/jupyter-spark.svg?branch=master)](https://travis-ci.org/mozilla/jupyter-spark)

[![codecov](https://codecov.io/gh/mozilla/jupyter-spark/branch/master/graph/badge.svg)](https://codecov.io/gh/mozilla/jupyter-spark)

Jupyter Notebook extension for Apache Spark integration.

Includes a progress indicator for the current Notebook cell if it invokes a
Spark job. Queries the Spark UI service on the backend to get the required
Spark job information.

![Alt text](/screenshots/ProgressBar.png?raw=true "Spark progress bar")

To view all currently running jobs, click the "show running Spark jobs"
button, or press ```Alt+S```.

![Alt text](/screenshots/SparkButton.png?raw=true "show running Spark jobs button")

![Alt text](/screenshots/Dialog.png?raw=true "Spark dialog")

A proxied version of the Spark UI can be accessed at
http://localhost:8888/spark.

## Installation

To install, simply run:

```
pip install jupyter-spark
jupyter serverextension enable --py jupyter_spark
jupyter nbextension install --py jupyter_spark
jupyter nbextension enable --py jupyter_spark
```

You **may also** have to enable the `widgetsnbextension` extension if it hasn't been enabled
before (check by running `jupyter nbextension list`):

```
jupyter nbextension enable --py widgetsnbextension
```

To double-check if the extension was correctly installed run:

```
jupyter nbextension list
jupyter serverextension list
```

Pleaes feel free to install [lxml](http://lxml.de/) as well to improve
performance of the server side communication to Spark using your favorite
package manager, e.g.:

```
pip install lxml
```

For development and testing, clone the project and run from a shell in the
project's root directory:

```
pip install -e .
jupyter serverextension enable --py jupyter_spark
jupyter nbextension install --py jupyter_spark
jupyter nbextension enable --py jupyter_spark
```

To uninstall the extension run:

```
jupyter serverextension disable --py jupyter_spark
jupyter nbextension disable --py jupyter_spark
jupyter nbextension uninstall --py jupyter_spark
pip uninstall jupyter-spark
```

## Configuration

To change the URL of the Spark API that the job metadata is fetched from
override the `Spark.url` config value, e.g. on the command line:

```
jupyter notebook --Spark.url="http://localhost:4040"
```

## Changelog

### 0.3.0 (2016-07-04)

- Rewrote proxy to use an async Tornado handler and HTTP client to fetch
  responses from Spark.

- Simplified proxy processing to take Amazon EMR proxying into account

- Extended test suite to cover proxy handler, too.

- Removed requests as a dependency.

### 0.2.0 (2016-06-30)

- Refactored to fix a bunch of Python packaging and code quality issues

- Added test suite for Python code

- Set up continuous integration: https://travis-ci.org/mozilla/jupyter-spark

- Set up code coverage reports: https://codecov.io/gh/mozilla/jupyter-spark

- Added ability to override Spark API URL via command line option

- **IMPORTANT** Requires manual step to enable after running pip install
  (see installation docs)!

  To update:

  1. Run `pip uninstall jupyter-spark`
  2. Delete `spark.js` from your `nbextensions` folder.
  3. Delete any references to `jupyter_spark.spark` in
     `jupyter_notebook_config.json` (in your .jupyter directory)
  4. Delete any references to `spark` in `notebook.json`
     (in .jupyter/nbconfig)
  5. Follow installation instructions to reinstall

### 0.1.1 (2016-05-03)

- Initial release with a working prototype
