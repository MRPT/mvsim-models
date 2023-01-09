#!/bin/bash

llgal -su --gc

rm -fr thumbs
mv .llgal thumbs

sed -i 's/\.llgal/thumbs/g' index.html
