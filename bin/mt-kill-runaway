#!/bin/bash
ps aux | grep main.py | head -1 | sed 's/ \+/	/g' | cut -f2 | xargs kill -9
