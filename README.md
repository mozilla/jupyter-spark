# jupyter-spark

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)
[![Build Status](https://travis-ci.org/mozilla/jupyter-spark.svg?branch=master)](https://travis-ci.org/mozilla/jupyter-spark)
[![codecov](https://codecov.io/gh/mozilla/jupyter-spark/branch/master/graph/badge.svg)](https://codecov.io/gh/mozilla/jupyter-spark)

**NOTE: This project is currently unmaintained, if anyone would like to take over maintenance please [let us know](https://github.com/mozilla/jupyter-spark/issues/55).**

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
jupyter nbextension enable --py widgetsnbextension
```

The last step is needed to enable the `widgetsnbextension` extension that
Jupyter-Spark depends on. It may have been enabled before by a different
extension.

You may want to append ``--user`` to the commands above if you're getting
configuration errors upon invoking them.

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

The Spark API that the job metadata is fetched from can be different for each SparkContext. As default, for the first Spark context uses port 4040, for the second 4041 and so on. If however `spark.ui.port` is set to 0 in SparkConf, Spark will choose a random ephemeral port for the API. 

In order to support this behaviour (and allow more than one tab in Jupyter with a SparkContext) load the jupyter spark extension

```python
%load_ext jupyter_spark
```

For Spark 2 use the provided magic without parameter

```python
%spark_progress
```
For Spark 1 provide the Spark API URL (e.g. `http://localhost:4040`)

```python
%spark_progress http://<spark-api-server>:<port>
```

To turn it off again use

```python
%spark_progress None
```

Note, these commands are line magics and need to have their own cell.

## Example

There is a simple `pyspark` example included in `examples` to confirm that your
installation is working.

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
