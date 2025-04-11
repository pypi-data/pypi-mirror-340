#!/usr/bin/env python


#===========================================================================#
#                                                                           #
#  File:       setup.py                                                     #
#  Usage:      install the files as a lib and generate excutables           #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       Jun 04, 2023                                                 #
#                                                                           #
#===========================================================================#


import os
import glob
import platform
from distutils.core import setup
#from setuptools import setup


def write_code_info(kwargs_setup):
    with open('pysupercell/__init__.py','w') as fw:
        for key in ['__name__','__version__','__author__','__author_email__','__url__','__license__','__platforms__']:
            print ('{:<20s}  =  "{}"'.format(key,kwargs_setup[key.strip('__')]),file=fw)



core_modules = [item.removesuffix('.py') for item in glob.glob('pysupercell/*py')]
util_modules = [item.removesuffix('.py') for item in glob.glob('pysupercell/utility/*py')]


kwargs_setup=dict(
name='PySupercell',
version='0.0.33',
author='Shunhong Zhang',
author_email='zhangshunhong.pku@gmail.com',
url='https://pypi.org/project/PySupercell',
download_url='https://pypi.org/project/PySupercell',
keywords=['Python','Crystal structure','supercell'],
py_modules=core_modules + util_modules,
license="MIT License",
description='Python library for creating and manipulating crystal structures',
long_description="""
An open-source Python library for playing with crystal structures, 
such as supercell, dislocation, slab, and nanotube""",
platforms=[platform.system()],
)


if __name__=='__main__':
    write_code_info(kwargs_setup)
    setup(**kwargs_setup)

