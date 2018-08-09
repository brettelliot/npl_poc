from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='npl_poc',
      version='0.1',
      description='NPL POC',
      long_description=readme(),
      url='http://github.com/brettelliot/npl_poc',
      author='Brett Elliot',
      author_email='brett@theelliots.net',
      license='MIT',
      packages=['npl_poc'],
      install_requires=[
          'markdown',
          'requests'
      ],
      include_package_data=True,
      test_suite="tests",
      entry_points={
          'console_scripts': ['npl_poc=npl_poc.command_line:main'],
      },
      zip_safe=False)