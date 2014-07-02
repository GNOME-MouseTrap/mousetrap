#!/bin/bash
if [ $# -lt 1 ] || [ -z "$1" ] || [ ! -f "$1" ] ; then
    echo "Usage:  $(basename "$0") FILE"
    exit 1
fi
echo "from __future__ import unicode_literals" > temp
echo "from __future__ import print_function" >> temp
echo "from __future__ import absolute_import" >> temp
echo "from __future__ import division" >> temp
cat "$1" >> temp
mv temp "$1"
