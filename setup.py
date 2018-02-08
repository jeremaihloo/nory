from setuptools import setup

setup(name='nory',
      version='1',
      description='A web framework using asyncio',
      url='http://github.com/jeremaihloo/nory',
      author='jeremaihloo',
      author_email='jeremaihloo1024@gmail.com',
      license='MIT',
      packages=['nory'],
      zip_safe=False,
      entry_points={
          'console_scripts': ['nory=nory.hotting:main'],
      }
      )
