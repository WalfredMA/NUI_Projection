#!/usr/bin/python2.7

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
	long_description = fh.read()


setup(
	name = 'NUI_projection',
	version = '0.0.2',
	author='Walfred MA',
	description = 'NUI projection tool based on recapture model',
	long_description=long_description,
	long_description_content_type="text/markdown",
	license = 'MIT License',
	url = 'https://github.com/WalfredMA/NUI_Projection',
	author_email="wangfei.ma@ucsf.com",
	packages = find_packages(),
	include_package_data = True,
	platforms = 'any',
	python_requires='>=2.7',
)

