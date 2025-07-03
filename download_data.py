import pandas as pd
import copernicusmarine
import numpy as np
from datetime import datetime
import pytz
from datetime import timedelta
#id dataset
#Colocar tu area de estudio
lon_min = -85
lon_max = -69
lat_min = -67
lat_max = 1.46

today=datetime.today().strftime("%Y-%m-%d")
future=(datetime.today() + timedelta(10)).strftime("%Y-%m-%d")

import os
# Obtener la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)


try:
    os.remove(f"{current_dir}/data/so_p.nc")
except:
    print("No habia data previa de salinidad")

try:
    os.remove(f"{current_dir}/data/thetao_p.nc")
except:
    print("No habia data de Temperatura")

id_dataset= "cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m"
copernicusmarine.subset(dataset_id = id_dataset,
                                  variables=["thetao"],
                        minimum_longitude = lon_min,
                        maximum_longitude = lon_max,
                        minimum_latitude = lat_min,
                        start_datetime = today,
                        end_datetime = today,
                        minimum_depth=0,
                        maximum_depth=5000,
                        maximum_latitude = lat_max,
                        #output_filename = f"thetao_p_{(datetime.today()).strftime("%Y%m%d")}.nc",
                        output_filename = f"thetao_p.nc",
                        output_directory = f"{current_dir}/data")


salinity_id="cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m"
copernicusmarine.subset(dataset_id = salinity_id,
                                  variables=["so"],
                        minimum_longitude = lon_min,
                        maximum_longitude = lon_max,
                        minimum_latitude = lat_min,
                        start_datetime = today,
                        end_datetime = today,
                        minimum_depth=0,
                        maximum_depth=5000,
                        maximum_latitude = lat_max,
                        output_filename = f"so_p.nc",
                        output_directory = f"{current_dir}/data")