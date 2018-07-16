"""
PyBuilder build file for "equities-etl"

Author: Abhishek Mishra (abhishekmishra3@gmail.com)
Date: 10/05/2018

"""

from pybuilder.core import use_plugin, init, Author

use_plugin('python.core')
use_plugin('python.install_dependencies')
use_plugin("python.distutils")

name = 'equities-etl'
authors = [Author('Abhishek Mishra', 'abhishekmishra3@gmail.com')]
license = 'GPL3'
summary = ''
url = 'https://github.com/abhishekmishra/equities-etl'
version = '0.0.1'

default_task = 'publish'

@init
def initialize (project):
    project.depends_on_requirements("requirements.txt")
