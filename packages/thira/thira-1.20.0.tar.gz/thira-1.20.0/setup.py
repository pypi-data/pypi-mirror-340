# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thira']

package_data = \
{'': ['*']}

install_requires = \
['tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['thira = thira.run:main'],
 'poetry.application.plugin': ['post_install = thira.install:install_binary']}

setup_kwargs = {
    'name': 'thira',
    'version': '1.20.0',
    'description': 'A Git hooks manager and commit message linter',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'your.email@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ervan0707/thira',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
