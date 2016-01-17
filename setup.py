from setuptools import setup

setup(
	name='mygpxdata',
	version='1.0.0',
	url='https://github.com/jimle-uk/mygpxdata',
	license='BSD',
	author='Jim Le',
	author_email='jim@heightdigital.co.uk',
	description='A gpx parser that outputs gpx trackpoints to svg and stats like distance, duration, splits, pace and climb',
	packages=['mygpxdata'],
	platforms='any',
	install_requires=[
		'pyparsing==2.0.7',
		'svgwrite==1.1.6'
	],
)