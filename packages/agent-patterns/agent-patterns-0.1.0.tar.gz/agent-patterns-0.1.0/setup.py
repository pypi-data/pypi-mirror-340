# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['agent_patterns', 'agent_patterns.core']

package_data = \
{'': ['*']}

install_requires = \
['langchain-openai>=0.3.12,<0.4.0',
 'langchain>=0.3.23,<0.4.0',
 'langgraph>=0.3.25,<0.4.0',
 'python-dotenv>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'agent-patterns',
    'version': '0.1.0',
    'description': 'This is a package of agents that can be extended to form agent implementations aligning with a number of ai agent design patterns.',
    'long_description': None,
    'author': 'osok',
    'author_email': 'michael@caughey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
