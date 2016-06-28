from setuptools import setup, find_packages

setup(
    name='jupyter-spark',
    version='0.2a1',
    description='Jupyter Notebook extension for Apache Spark integration',
    author='Mozilla Telemetry',
    author_email='telemetry@lists.mozilla.org',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    license='MPL2',
    install_requires=[
        'ipython >= 4',
        'jupyter',
        'notebook >= 4.2',
        'requests',
        'beautifulsoup4',
        'widgetsnbextension',
    ],
    url='https://github.com/mozilla/jupyter-spark',
    zip_safe=False,
)
