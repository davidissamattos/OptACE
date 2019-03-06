#!/usr/bin/env bash
#this requires that will install mongo and create the folder
#THis is script is mainly for the PyCharm debug features
export MONGODB="localhost:27017"
mkdir  -p ~/.mongo/data
mongod --dbpath ~/.mongo/data &