#
# ContaFi: Cliente de API en Python.
# Copyright (C) ContaFi <https://www.contafi.cl>
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la GNU Lesser General Public License (LGPL) publicada
# por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
# o (a su elección) cualquier versión posterior de la misma.
#
# Este programa se distribuye con la esperanza de que sea útil, pero SIN
# GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
# PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
# Public License (LGPL) para obtener una información más detallada.
#
# Debería haber recibido una copia de la GNU Lesser General Public License
# (LGPL) junto a este programa. En caso contrario, consulte
# <http://www.gnu.org/licenses/lgpl.html>.
#

# Always prefer setuptools over distutils
# To use a consistent encoding
"""
Setup script for the ContaFi API client.

This script is used to install the ContaFi API client package.
It includes the project information, dependencies, and setup instructions.

"""
from codecs import open as codecs_open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with codecs_open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

description = 'Cliente para realizar la integración con los '
description += 'servicios web de ContaFi desde Python.'

setup(

    name='contafi',

    # Versions should comply with PEP440
    version='2.0.0',

    description=description,
    long_description="\n"+long_description,

    # The project's main homepage.
    url='https://github.com/contafi/contafi-api-client-python',

    # Author details
    author='ContaFi',
    author_email='dev@contafi.cl',

    # Choose your license
    license='LGPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        # If you want to mark it as Beta, use: 'Development Status :: 4 - Beta'
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Lesser General Public License '
        'v3 or later (LGPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='sii chile bhe bte contafi facturacion '
    'contribuyentes boleta electronica',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # List run-time dependencies here
    install_requires=['requests'],

)
