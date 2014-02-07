from distutils.core import setup
import py2exe, sys, os

setup(console=['profile_change.py'],
      data_files=['cacert.pem'])
