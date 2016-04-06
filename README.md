# jupyter-spark
Jupyter Notebook extension for Apache Spark integration

Include a progress indicator for the current Notebook cell if it invokes a Spark job. Query the Spark UI service on the backend to get the required Spark job information.
<br/><br/><br/>
![Alt text](/screenshots/ProgressBar.png?raw=true "Spark progress bar")
<br/><br/><br/>
To view all currently running jobs, click the "show running Spark jobs" button, or press ```Alt+S```.
<br/><br/><br/>
![Alt text](/screenshots/SparkButton.png?raw=true "show running Spark jobs button")
<br/><br/><br/>
![Alt text](/screenshots/Dialog.png?raw=true "Spark dialog")
<br/><br/><br/>
NOTE: Uninstalling jupyter-spark via `pip uninstall jupyter-spark` will uninstall the server extension but leave the client extension in a partially installed state. To fully remove the extension:

1. Run `pip uninstall jupyter-spark`
2. Delete `spark.js` from your `nbextensions` folder.
3. Delete any references to `jupyter-spark.spark` in `jupyter_notebook_config.json` (in your .jupyter directory)
4. Delete any references to `spark` in `notebook.json` (in .jupyter/nbconfig)
