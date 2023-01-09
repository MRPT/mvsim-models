#!/bin/bash

tree -H '.' -L 1 --noreport --charset utf-8 -o index.html

#(cd textures-cgbookcase && ./build-index.sh)
(cd anims && tree -H '.' -L 1 --noreport --charset utf-8 -o index.html)

