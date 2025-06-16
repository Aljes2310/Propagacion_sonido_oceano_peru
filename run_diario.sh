#!/bin/bash -l
# Cargar entorno completo
source /home/user03/.bashrc

alias bellhop='/home/user03/siogas/Acoustics-Toolbox-main/Bellhop/bellhop.exe' 
export PATH="$PATH:/home/user03/siogas/Acoustics-Toolbox-main/Bellhop"

# Activar entorno virtual
#source /home/user03/siogas/myvenv/bin/activate

# Ejecutar scripts con rutas absolutas
/home/user03/siogas/myvenv/bin/python /home/user03/siogas/download_data.py
/home/user03/siogas/myvenv/bin/python /home/user03/siogas/generacion_imagenes.py
/home/user03/siogas/myvenv/bin/python /home/user03/siogas/siogas/map_generation.py



# callao siogas
/home/user03/siogas/myvenv/bin/python /home/user03/siogas/callao_generation.py
/home/user03/siogas/myvenv/bin/python /home/user03/siogas/siogas_callao/map_generation.py
