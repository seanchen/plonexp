from setuptools import setup, find_packages
import os

version = open(os.path.join('iscorpio/myworkshop', 'version.txt')).read()

setup(name='iscorpio.myworkshop',
      version=version,
      description="online service for publishing and managing workshop info and event",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Python Zope Plone Event Calendar',
      author='iScorpio',
      author_email='iscorpio@users.sourceforge.net',
      url='http://myworkshop.sourceforge.net',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['iscorpio'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
