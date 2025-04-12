#!/usr/bin/env python3
import setuptools
# import distutils.command.install_lib
# from distutils.core import setup
import os

def find (p, d):
    ret = []
    for b, dd, ff in os.walk(os.path.join(p, d)):

        for f in ff:
            if not f.startswith("."):
                fp = os.path.join(b, f)
                ret.append(os.path.relpath(fp, p))
    ret.sort()
    # for x in ret[:10]:
    #     print "**", x
    return ret

setuptools.setup(
    name='etherdump',
    version='0.3.0',
    author='Active Archives Contributors',
    author_email='mm@automatist.org',
    packages=['etherdump', 'etherdump.commands'],
    package_dir={'etherdump': 'etherdump'},
    #package_data={'activearchives': find("activearchives", "templates/") + find("activearchives", "data/")},
    package_data={'etherdump': find("etherdump", "data/")},
    scripts=['bin/etherdump'],
    url='http://activearchives.org/wiki/Etherdump',
    license='LICENSE.txt',
    description='Etherdump an etherpad publishing & archiving system',
    # long_description=open('README.md').read(),
    install_requires=[
         "html5lib", "jinja2", "python-dateutil", "requests", "pyyaml"
    ]
)
