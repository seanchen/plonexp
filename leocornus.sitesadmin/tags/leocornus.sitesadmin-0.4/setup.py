from setuptools import setup, find_packages
import os

version = open(os.path.join('leocornus/sitesadmin', 'version.txt')).read()

setup(name='leocornus.sitesadmin',
      version=version,
      description="Providing facilities, tools, etc. for Plone sites administration",
      long_description=open(os.path.join('leocornus/sitesadmin', "README.txt")).read() + "\n" +
                       open(os.path.join("leocornus/sitesadmin", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Python Plone Zope Sites Administration Hosting',
      author='Sean Chen',
      author_email='sean.chen@leocorn.com',
      url='http://plonexp.leocorn.com/sitesadmin',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['leocornus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.membrane',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
