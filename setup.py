from setuptools import setup, find_packages
import sys, os

version = '1.0'

long_description = open('README.rst').read()

setup(
      name='afb-to-xlsx',
      version=version,
      description="CFONB to CSV & XLSX converter based in Python-CFONB by Florent Pigout.",
      long_description=long_description,
      classifiers=[],
      keywords='cfonb bank statement parser gui csv',
      author='Florent Pigout, Fernando Mendez',
      author_email='fpigout@anybox.fr',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite = "cfonb.tests.test_all.suite"
      )
