#!/usr/bin/env bash

conda activate sketcher-3 #python-3
pip install opencv-contrib-python #(v4)
conda install -c menpo opencv3 #(v3)
conda install -c conda-forge opencv==3.4.2
conda install -c conda-forge keras
conda install -c anaconda pillow
conda install -c conda-forge matplotlib
conda install -c conda-forge scipy
#conda deactivate