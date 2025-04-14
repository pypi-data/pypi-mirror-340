from setuptools import setup, find_packages

setup(
    name="go_data_creator_for_algotrade",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pymssql",
        "pandas"
    ],
    author="okan.uregen",
    description="A data creation and formatting tool for algo trading",
    long_description="A tool for reading and formatting data from SQL Server for algorithmic trading.",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
