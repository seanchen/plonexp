# setup.py

"""
Python setup script based on setuptools.
"""

from setuptools import setup, find_packages
import os

version = open(os.path.join("iscorpio/plonepas", "version.txt")).read()

setup(name='iscorpio.plonepas',
      version=version,
      description="Plone PAS Playground",
      long_description=open(os.path.join("iscorpio/plonepas", "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Python Zope Plone PAS',
      author='Sean Chen',
      author_email='chyxiang@gmail.com',
      url='',
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
