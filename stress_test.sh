#!/bin/bash
max=10000
for i in `seq 1 $max`
do
  curl localhost:5000
  sleep $1
done