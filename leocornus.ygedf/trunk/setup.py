
# setup.py

from setuptools import setup, find_packages
import os

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"


prodFolder = 'leocornus/ygedf'

setup(name='leocornus.ygedf',
      version=open(os.path.join(prodFolder, 'version.txt')).read(),
      description="Providing themes, facilities, tools, etc. for ygedf.org websites",
      long_description=open(os.path.join(prodFolder, "README.txt")).read() + "\n" +
                       open(os.path.join(prodFolder, "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules :: Theme",
        ],
      keywords='Python Plone Zope Skin Theme',
      author='Sean Chen',
      author_email='sean.chen@leocorn.com',
      url='http://plonexp.leocorn.com/ygedf',
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
