#!/bin/bash

set -e

# Verifica si el entorno nao_py27 ya existe
if conda info --envs | grep -q "^nao_py27"; then
    echo "⚠️ El entorno 'nao_py27' ya existe. Se omitirá su creación."
else
    echo "🔧 Creando entorno 'nao_py27' con Python 2.7..."
    conda create -y -n nao_py27 python=2.7
    echo "Entorno 'nao_py27' creado."
fi

echo "📦 Instalando requirements_nao.txt en 'nao_py27'..."
conda activate nao_py27 || source activate nao_py27
pip install -r requirements_nao.txt
conda deactivate
echo "✅ Requisitos instalados en 'nao_py27'."

# Verifica si el entorno nao_sv ya existe
if conda info --envs | grep -q "^nao_sv"; then
    echo "⚠️ El entorno 'nao_sv' ya existe. Se omitirá su creación."
else
    echo "🔧 Creando entorno 'nao_sv' desde environment.yml..."
    conda env create -n nao_sv -f environment.yml
    echo "✅ Entorno 'nao_sv' creado."
fi

echo -e "\n Instalación completada."
echo " Activa el entorno py3 con: conda activate nao_sv"
echo " Luego corre: python api_emocion.py"
echo " Después ejecuta: ./run.sh para lanzar el flujo general"
