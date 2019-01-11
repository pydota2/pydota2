#!/bin/bash

# build dotaservice egg
cd dotaservice
pip3 install -e .
cd ..

# build dotaworld egg
cd dotaworld
pip3 install -e .
cd ..

# build pydota2 egg
pip3 install -e .
