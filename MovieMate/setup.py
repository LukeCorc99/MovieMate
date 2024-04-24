from setuptools import setup

# Setup.py is used to create local packages required using my virtual environment.

# Define author name and source repository
AUTHORNAME = 'Luke Corcoran'
SRCREPO = 'src'

# Requirements package we will use for the web app.
# Streamlit is a python library that allows you to build web apps from python scripts
LISTOFREQUIREMENTS = ['streamlit']

# Setup configuration
setup(
    name=SRCREPO,
    version='0.1',
    author=AUTHORNAME,
    description='A movie recommender application which gives recommendations based on movies entered by user.',
    package=[SRCREPO],
    python_requires='>=3.6',
    install_requires=LISTOFREQUIREMENTS,
)
