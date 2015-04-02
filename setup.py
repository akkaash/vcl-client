
from setuptools import setup, find_packages
import sys, os

setup(name='vcl',
    version='0.1',
    description="VCL Client",
    long_description="VCL Client",
    classifiers=[],
    keywords='',
    author='Akkaash Goel',
    author_email='goel.akkaash@gmail.com',
    url='https://github.com/akkaash',
    license='BSD-3-Clause',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        ### Required to build documentation
        # "Sphinx >= 1.0",
        ### Required for testing
        "nose",
        "coverage",
	    'click'
        ],
    setup_requires=[],
    entry_points="""
        [console_scripts]
        vcl=vcl.vcl:cli
    """,
    namespace_packages=[],
    )
