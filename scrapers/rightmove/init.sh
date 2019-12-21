#!/bin/bash

# Init active
for file in ./data/*
    do
      python3 init_active.py $file
    done

# Init sold
