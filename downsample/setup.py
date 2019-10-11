import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="example-pkg-your-username",
	version="0.0.1",
	author="Walfred MA",
	author_email="wangfei.ma@ucsf.com",
	description="downsampleing tool based on recapture model",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/WalfredMA/Saturation-Projection-for-NUI-insertion-discovery/tree/master/downsample",
	packages=setuptools.find_packages(),
	python_requires='>=2.7',
)
