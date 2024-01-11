#!/bin/bash -l

#Call this as bash -l run.bash

echo Conda Activate
conda activate website
echo "Sourcing"
source /home/fergal/all/websitegen/setup.src
echo Running
cd /home/fergal/all/websitegen/py
/home/fergal/all/websitegen/py/main.py
echo "Cleaning up"
conda deactivate
