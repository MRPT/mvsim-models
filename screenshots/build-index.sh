#!/bin/bash

llgal -suaf

rm -fr thumbs
mv .llgal thumbs

sed -i 's/\.llgal/thumbs/g' index.html
