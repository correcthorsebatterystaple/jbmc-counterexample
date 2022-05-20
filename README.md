About
=====
JBMC-CounterExample is a tool for generating valid Java counterexamples from the output of JBMC. It runs JBMC on a specified Java file and then processes the produced output to identify the counterexamples and generate a separate Java file for each counterexample found.

Usage
=====
In order to run the tool you'll need to download Python 3.
To run the JBMC-CounterExample tool for a specific example you have to mount into the directory of the Java file that is to be tested by JBMC. Afterwards you simply execute the cbmc_parser.py file located in the src folder of the repository as follows:

`python3 <Path-to-cbmc_parser.py> <Path-to-JBMC-executeable> <Name-of-file-to-be-tested>`

The tool will then compile the class and its requirements, run JBMC on it, extract the counterexamples from JBMC's output, and produce a valid, runnable Java counterexample.
