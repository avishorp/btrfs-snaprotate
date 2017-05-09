#!/usr/bin/env python

from distutils.core import setup

setup(name="btrfs_snaprotate",
      version="0.9",
      description="BTRFS Sanpshot creation and rotation tool",
      author="Avishay Orpaz",
      author_email="avishorp@gmail.com",
      scripts=['btrfs_snaprotate'],
      packages=['btrfs'],
      install_requires=['python-dateutil'],
      license="MIT",
      platforms=['linux']
      )
