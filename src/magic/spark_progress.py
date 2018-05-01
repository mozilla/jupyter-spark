from __future__ import print_function

from ipykernel.comm import Comm
from IPython import get_ipython
from IPython.core.magic import Magics, line_magic, magics_class


@magics_class
class SparkProgress(Magics):

    @line_magic
    def spark_progress(self, line):
        """Toggle Spark progress being shown under cells"""

        comm = Comm(target_name='spark_comm')
        if line.startswith("http"):
            url = line
        else:
            param = globals().get(line, None)
            if type(param).__name__ == "SparkContext":
                url = param.uiWebUrl
            elif type(param).__name__ == "SparkSession":
                url = param.sparkContext.uiWebUrl
            else:
                url = None

        comm.send({'uiWebUrl': url})

        if url is None:
            print("No Spark Context given as parameter, turning Spark progress monitoring off")
        else:
            print("Spark progress monitoring turned on")

        comm.close()


ip = get_ipython()
ip.register_magics(SparkProgress)
