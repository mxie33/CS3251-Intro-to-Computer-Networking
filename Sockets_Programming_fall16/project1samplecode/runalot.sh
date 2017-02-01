#!/bin/bash

i=0
loop=$1

while [ $i -lt $loop ]
do
  python client.udp.example.py -m $i;
  i=$(( $i + 1 ))
done;
