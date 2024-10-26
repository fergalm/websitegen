#!/bin/bash -l

#Call this as bash -l run.bash

echo "Running at"
date 
echo Conda Activate
conda activate website
echo "Sourcing"
source /home/fergal/all/websitegen/setup.src
echo Running
cd /home/fergal/all/websitegen/bin/
/home/fergal/all/websitegen/bin/mls.py
echo "Cleaning up"
conda deactivate
