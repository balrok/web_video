#!/usr/bin/env python3

from distutils.core import setup
import pip
import re
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=pip.download.PipSession())
reqs = [str(ir.req) for ir in install_reqs]

lib = "web_video"
with open(lib + '/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(name=lib,
    version=version,
    description='Converts videos and jpg in a folder to be great for the web',
    long_description=readme,
    author='Carl Mai',
    author_email='carl.schoenbach@gmail.com',
    url='https://balrok.com',
    install_requires=reqs,
    packages=[lib],
    entry_points = {
        'console_scripts': [
            'web_video = web_video.run:run',                  
        ],              
    },
    classifiers=[
                'Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'Environment :: Console', 
                'License :: OSI Approved :: MIT License',
                'Topic :: Multimedia :: Graphics',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.5',
    ],
   )
