from setuptools import setup, find_packages
import os

version = open(os.path.join("iscorpio/plonerm", "version.txt")).read()

setup(name='iscorpio.plonerm',
      version=version,
      description="Resource Management System on Plone Platform",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Python Zope Plone Resource Management',
      author='iscorpio',
      author_email='iscorpio@users.sourceforge.net',
      url='http://plonerm.sourceforge.net',
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
