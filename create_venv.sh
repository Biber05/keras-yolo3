#!/usr/bin/env bash

python3 -m venv ./venv
source ./venv/bin/activate

pip3 install wheel
pip3 install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.6.0-py3-none-any.whl
pip3 install "keras==2.1.5"
pip3 install pillow
pip3 install matplotlib
pip3 install h5py