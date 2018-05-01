.PHONY: install build uninstall enable clean dev

install:
	jupyter serverextension enable --py jupyter_spark
	jupyter nbextension install --py jupyter_spark
	jupyter nbextension enable --py jupyter_spark
	@echo ""
	@echo "NOTE: Copy ./src/magic/spark_progress.py into the startup folder, e.g. ~/.ipython/profile_default/startup/"
	@echo ""

uninstall:
	jupyter serverextension disable --py jupyter_spark
	jupyter nbextension disable --py jupyter_spark
	jupyter nbextension uninstall --py jupyter_spark
	pip uninstall -y jupyter-spark
	@echo ""
	@echo "NOTE: Remove spark_progress.py from startup folder, e.g. ~/.ipython/profile_default/startup/"
	@echo ""

clean: uninstall
	rm -rf dist/

build: clean
	python setup.py sdist
	pip install dist/*.tar.gz

dev: build install

notebook:
	jupyter notebook
