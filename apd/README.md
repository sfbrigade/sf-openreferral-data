Adult Probation Department (APD) Source Data Parsing Tools
=================================

This directory contains resources related to the parsing of the source Getting Out and Staying Out guide data.  

Some highlights:

1.  apd_parser.py : the script that does the transformation from text to json ready for import to Ohana
2.  FullExport_servicesOnly....txt : the source data extracted from the MS Word doc to text
3.  open_ref.json : the output from running the apd_parser.py script on the source data file.  This should be ready for import into Ohana.  
4.  tests : folder that contains test files for the importer.  To run the test cd into the apd folder and run py.test.

#Instructions for setting up py.test on your computer

There can be an issue with PYTHONPATH and running the tests.  Best chance at success is to run this from the root of the repository:

PYTHONPATH="./apd" py.test


