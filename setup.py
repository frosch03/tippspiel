from setuptools import setup

setup(name='tippspiel',
      version='0.1',
      description='A simple app to track a football bet games',
      url='http://github.com/frosch03/tippspiel',
      author='Matthias Brettschneider',
      author_email='frosch03@frosch03.de',
      license='BSD',
      packages=['tippspiel'],
      entry_points={
          'console_scripts': ['tipps=tippspiel.command_line:main']
      },
      zip_safe=False)
