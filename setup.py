from setuptools import find_packages, setup

setup(
    name='jupyter-spark',
    version='0.3.0',
    description='Jupyter Notebook extension for Apache Spark integration',
    author='Mozilla Firefox Data Platform',
    author_email='fx-data-platform@mozilla.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    license='MPL2',
    install_requires=[
        'ipython >= 4',
        'jupyter',
        'notebook >= 4.2',
        'beautifulsoup4',
        'widgetsnbextension',
    ],
    url='https://github.com/mozilla/jupyter-spark',
    zip_safe=False,
)
