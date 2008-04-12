#!/usr/bin/env python

DEBUG = True

from distutils.core import setup

ver='0.3'

setup(name="pyreg",
       version=ver,
       description="Registry wrapper classes",
       author="Jamie Bliss",
       author_email="astronouth7303+pyreg@gmail.com",
       url="http://www.astro73.com/download/pyreg/",
       download_url="http://www.astro73.com/download/pyreg/pyreg-"+ver+".zip",
       long_description="""``pyreg`` defines classes to wrap ``_winreg`` in a more friendly interface,
including demunging data. Example:

>>> from pyreg import *
>>> HKEY_LOCAL_MACHINE / 'Software' / 'Python' / 'PythonCore' / '2.5' / 'InstallPath' | None
u'c:\\Python25\\'

See http://www.astro73.com/download/pyreg/readme.html for help or try

>>> help('pyreg')

You may file bug reports to the author's address.""",
       packages=['pyreg'],
       package_dir={'pyreg': 'src/pyreg'},
       platforms=['Microsoft Windows'],
       license='GNU General Public License',
#       requires='_winreg',
       classifiers=['Development Status :: 3 - Alpha',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: GNU General Public License (GPL)',
                    'Operating System :: Microsoft :: Windows',
                    'Programming Language :: Python',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                    'Topic :: System',
                    'Topic :: System :: Systems Administration']
      )
