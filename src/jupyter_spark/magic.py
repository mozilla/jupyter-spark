from __future__ import print_function

from ipykernel.comm import Comm
from IPython.core.magic import Magics, line_magic, magics_class


@magics_class
class SparkProgress(Magics):

    def init(self, line=""):
        """Start Spark progress if possible"""
        comm = Comm(target_name='spark_comm')
        if line.startswith("http"):
            url = line
        else:
            from pyspark import SparkContext
            # Using an internal API to avoid asking the user for the SparkContext variable
            # TODO: Try to find a way without using an internal API
            sc = SparkContext._active_spark_context
            if sc is not None:
                url = sc.uiWebUrl
            else:
                url = None

        comm.send({'uiWebUrl': url})

        if url is None:
            print("No Spark Context found")
        else:
            print("Spark progress monitoring turned on")

        comm.close()

    @line_magic
    def spark_progress(self, line):
        """Toggle Spark progress being shown under cells"""
        self.init(line)
