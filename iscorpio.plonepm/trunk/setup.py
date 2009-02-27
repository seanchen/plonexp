from setuptools import setup, find_packages
import os

version = open(os.path.join('iscorpio/plonepm', 'version.txt')).read()

setup(name='iscorpio.plonepm',
      version=version,
      description="A Plone way to manage project",
      long_description=open(os.path.join('iscorpio/plonepm', "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Python Plone Zope Project Management',
      author='iScorpio',
      author_email='iscorpio@users.sourceforge.net',
      url='http://plonexp.sourceforge.net',
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

      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )
