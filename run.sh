#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAOQI_DIR="${SCRIPT_DIR}/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327"

# Activar entorno conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nao_py27

# Configurar entorno de NAOqi
export PYTHONPATH="${PYTHONPATH}:${SCRIPT_DIR}/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/lib/python2.7/site-packages"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${SCRIPT_DIR}/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/lib"


# Ejecutar usando el Python del entorno actual
python main.py
