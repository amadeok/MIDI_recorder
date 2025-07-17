# setup.py

from setuptools import setup, find_packages

setup(
    name='PyMidiRec',  # Name of your module
    version='0.1',  # Version number
    packages=find_packages(),  # Find packages in the current directory
    description='A simple Python module with useful functions',
    long_description_content_type='text/markdown',
    author='Your Name',  # Your name or your organization's name
    author_email='your.email@example.com',  # Your email
    url='https://github.com/yourusername/mymodule',  # URL to your project
    classifiers=[
    ],
    install_requires=[],  # Any dependencies your module has
    python_requires='>=3.6',  # Minimum Python version required
)
