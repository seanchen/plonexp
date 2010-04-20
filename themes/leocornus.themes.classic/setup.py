
# setup.py

from setuptools import setup, find_packages
import os

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

theFolder = "leocornus/themes/classic"

setup(name='leocornus.themes.classic',
      version=open(os.path.join(theFolder, "version.txt")).read().split('\n')[0],
      description="Leocornus classic Plone 3 theme",
      long_description=open(os.path.join(theFolder, "README.txt")).read() +
                       "\n" +
                       open(os.path.join(theFolder, "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules :: Theme",
        ],
      keywords='Zope Plone Python Theme Web',
      author='Sean Chen',
      author_email='sean.chen@leocorn.com',
      url='http://plonexp.svn.sourceforge.net/svnroot/plonexp/themes/leocornus.themes.classic',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['leocornus'],
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
