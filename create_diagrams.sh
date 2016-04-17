#!/bin/bash

pyreverse -o svg -k -p bitween_small bitween/
pyreverse -o svg -s1 -p bitween bitween/
pyreverse -o svg -s1 -a1 -p bitween_big bitween/ 
