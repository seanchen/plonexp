from setuptools import setup, find_packages
import os

version = '0.1'

setup(name = 'iscorpio.sandbox',
      version = version,
      description = "",
      long_description = open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers = [
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords = 'Python',
      author = 'iscorpio',
      author_email = 'i.qian.wang@gmail.com',
      url = 'http://shellconsole.svn.sourceforge.net/svnroot/shellconsole/iscorpio.sandbox/',
      license = 'GPL',
      packages = find_packages(exclude = ['ez_setup']),
      namespace_packages = ['iscorpio'],
      include_package_data = True,
      zip_safe = False,
      install_requires = [
        'setuptools',
        # -*- Extra requirements: -*-
      ],
      entry_points = """
      # -*- Entry points: -*-
      """,
      )
