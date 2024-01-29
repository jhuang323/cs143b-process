# CS143B Project 1 Process and Resource Mangement README

## Setup
Note: This project is written entirely in python on OpenLab machines. It is recommended to run this project on the UCI Openlab machines.

### Steps to Setup/Run
1. Extract the zip file that was submitted to canvas by huangjk2@uci.edu (ID: 67387111) inside there should be the source code for Project 1

Note: No compilation is necessary for python
- Must use redirection operators ("<",">") to redirect in an input file and to write to an output file
2. main.py is the shell. To run you must use the redirection operator < to redirect in an input file to stdin and > to redirect stdout to an output file

An example of running the program:
```
python main.py <in.txt >out.txt
```
Assuming in.txt contains valid commands according to specifications it will write the output to out.txt

## Structure of Program
- main.py

The shell of the program takes in commands from stdin and outputs the output to stdout after each command
- manager.py

The Process and Resource manager. This class is responsible for implementing all the functions such as creat,delete,request,delete,timeout,etc. It is used to manager process and resources using a 3 level ready list
- aresource.py

Defines the resource class with all appropiate instance variables and methods to manage a resource.
- process.py

Defines the process class with all appropiate instance variables and methods to manager a process.