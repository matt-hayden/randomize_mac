import os, os.path
from setuptools import find_packages, setup

setup(name='RandomizeMAC',
      version = "1.0a1",
      description='Daily random MACs by interface and wifi network',
      url='https://github.com/matt-hayden/randomize_mac',
      maintainer="Matt Hayden (Valenceo, LTD.)",
      maintainer_email="github.com/matt-hayden",
      license='Unlicense',
      packages=find_packages(exclude='contrib docs tests'.split()),
      entry_points = {
          'console_scripts': [
              'randomize_mac=randomize_mac.cli:randomize_networks',
              ]
          },
      package_data = {
          'randomize_mac': ['etc/*'],
          },
      install_requires = [ 'docopt' ],
      zip_safe=True,
     )
