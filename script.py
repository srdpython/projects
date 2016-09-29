#!/usr/bin/env python
import argparse
import os
parser=argparse.ArgumentParser()
parser.add_argument("--directory")
parser.add_argument("--showdir")
args=parser.parse_args()
if args.directory:
  print "the directory is", os.getcwd()
