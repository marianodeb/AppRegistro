#!/usr/bin/env bash


# 1. Nos movemos a la carpeta donde está este script
cd "$(dirname "$0")"

# 2. Activamos el entorno virtual usando tu nombre correcto (.venv)
source .venv/bin/activate

# 3. Ejecutamos la app de escritorio en segundo plano
python app_tkgestor.py &

# 4. Ejecutamos Streamlit
streamlit run appST_web.py
