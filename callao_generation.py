import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import math
import arlpy.uwapm as pm
import numpy as np

ds_thetao=xr.open_dataset("./data/thetao_p.nc").sel(latitude=slice(-13, -11))
ds_so=xr.open_dataset("./data/so_p.nc").sel(latitude=slice(-13, -11))

puntos_grilla=ds_thetao.isel(time=0, depth=4).to_dataframe().reset_index().dropna().reset_index(drop=True)

# Calculando velocidad del sonido
ds_sound_profile= 1449 + 4.67*ds_thetao["thetao"] - 0.055*(ds_thetao["thetao"]**2)+0.0003*(ds_thetao["thetao"]**3) + (1.39-0.012*ds_thetao["thetao"])*(ds_so["so"]-35) +0.017*ds_so["depth"]

del ds_thetao, ds_so

# Importando batimetria
bati=xr.open_dataset("/home/user03/siogas/data/Bati_peru_1km_SRTM30.nc")

"""
#Importando coordenadas de puntos de grilla
puntos_grilla=pd.read_csv("./data/Puntos_grilla_callao.csv")
puntos_grilla['latitude'] = puntos_grilla['latitude'].astype(float)
puntos_grilla['longitude'] = puntos_grilla['longitude'].astype(float)
"""


# Interpolado profundidades
import numpy as np
new_depths=np.arange(1,5000,10)
ds_sound_profile=ds_sound_profile.interp(depth=new_depths)
#pasando a df
ds_sound_profile=ds_sound_profile.to_dataframe(name="Sound Velocity(m/s)").dropna().reset_index()

ds_sound_profile["latitude"]=ds_sound_profile['latitude'].astype('float64')
ds_sound_profile["longitude"]=ds_sound_profile['longitude'].astype('float64')
ds_sound_profile["time"]=np.datetime_as_string(ds_sound_profile["time"], unit='D')


for i in range(0,len(puntos_grilla),1):
    # Seleccionando perfil
    perfil=ds_sound_profile[(ds_sound_profile["latitude"]==puntos_grilla["latitude"][i]) 
                        & (ds_sound_profile["longitude"]==puntos_grilla["longitude"][i])
                        & (ds_sound_profile["time"]==ds_sound_profile["time"].min())].reset_index(drop=True)

    if len(perfil)>3: 
        # seleccionando el punto mas cercano al nodo del perfil acustico
        df_bati_pto=bati.sel(lon=slice(perfil["longitude"].unique().item() - 2, perfil["longitude"].unique().item())).sel(lat=perfil["latitude"].unique().item(), method="nearest").to_dataframe().reset_index()
        # calculando la distancia de los nodos mas cercanos en la misma latitud
        df_bati_pto["distance_m"]=(abs(df_bati_pto["lon"] - perfil["longitude"].unique().item())*111.32)*1000 #pasando de grados decimales a km a m
        df_bati_pto["elev"]=abs(df_bati_pto["elev"])
        df_bati_pto=df_bati_pto.sort_values(by="distance_m").reset_index(drop=True)

        # Manejo de posible error cuando la interpolacion del perfil del sonido excede la batimetira
        if df_bati_pto["elev"].max() <= perfil["depth"].max():
            perfil=perfil[~(perfil["depth"]>=df_bati_pto["elev"].max())].reset_index(drop=True)
            print("Dato Modelo Numerico excedia la batimetria")
        else :
            pass

        # Parseando batimetria al formato que pide env
        bat_list=[]
        for i in range(len(df_bati_pto)):
            elev_nested=[df_bati_pto["distance_m"][i], abs(df_bati_pto["elev"][i])]
            bat_list.append(elev_nested)
            
        bat_list = [sublista for sublista in bat_list if not any(math.isnan(x) for x in sublista)]
        bat_list[0][0]=0

        # Parseando perfiles acusticos
        ssp=[]
        for i in range(0, len(perfil),1):
            nested_list=[perfil["depth"][i], perfil["Sound Velocity(m/s)"][i]]
            ssp.append(nested_list)

        ssp[0][0]=0
        ssp[-1][0]=abs(round(df_bati_pto["elev"].max(),0))
        ssp = sorted(ssp, key=lambda x: x[0])

        # Eliminar duplicados conservando el primer valor
        seen = set()
        ssp_unique = []
        for item in ssp:
            depth = item[0]
            if depth not in seen:
                seen.add(depth)
                ssp_unique.append(item)

        
        # Definiendo env
        env = pm.create_env2d(
            depth=bat_list,
            soundspeed=ssp_unique,
            bottom_soundspeed=1450,
            bottom_density=1200,
            bottom_absorption=1.0,
            tx_depth=5 # profundidad transmisor
            )
        
        
        env['frequency']=2100
        env['rx_range'] = np.linspace(0, 5000, 100) # x (metros)
        #df_bati_pto["elev"].max() , perfil["depth"].max()
        env['rx_depth'] = np.linspace(0, abs(perfil["depth"].max()), 100) # y (metros)

        tloss = pm.compute_transmission_loss(env)

        # Obtener los valores absolutos (módulo) de la transmisión
        tloss_db = -20 * np.log10(np.abs(tloss))

        # Crear los ejes (depth y range)
        depth = tloss.index.values
        range_ = tloss.columns.values

        extent=[0, 5, depth.min(), depth.max()]

        # Crear el gráfico
        f, (a1, a2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 3]}, dpi=150, figsize=(15,6))
        f.subplots_adjust(wspace=0.2)

        # Gráfico principal (contourf)
        img = a2.contourf(tloss_db, extent=extent, cmap='jet_r', extend="max", levels=np.arange(0, 120, 5))
        a2.invert_xaxis()  # Invertir eje X
        a2.invert_yaxis()  # Invertir eje Y
        # Barra de color
        cbar = f.colorbar(img, ax=a2, label='Pérdida del sonido (dB)')
        cbar.set_ticks(np.arange(0, 115, 10))
        # Etiquetas y título
        a2.set_xlabel('Rango (km)')
        a2.set_ylabel('Profundidad (m)')
        a2.set_title(f'Latitud: {perfil["latitude"].unique().item()}   Longitud: {perfil["longitude"].unique().item()}    f=2100 Hz')

        ### Perfil
        #perfil_10=ds_sound_profile[(ds_sound_profile["latitude"]==puntos_grilla["latitude"][i]) & (ds_sound_profile["longitude"]==puntos_grilla["longitude"][i])
        #                        & (ds_sound_profile["time"]==ds_sound_profile["time"].max())].reset_index(drop=True)

        a1.plot(perfil["Sound Velocity(m/s)"], perfil["depth"], "-r", label=perfil.time.unique())
        #a1.plot(perfil_10["Sound Velocity(m/s)"], perfil_10["depth"], "-b", label=perfil_10.time.unique())
        #a1.ylim([0,300])
        a1.invert_yaxis()
        a1.set_ylabel("Profundidad(m)")
        a1.set_xlabel("Velocidad del Sonido (m/s)")
        a1.grid(which="both", alpha=0.6)
        a1.legend(loc="lower left")
        a1.set_ylim([depth.max(),0])


        # Guardar la figura (descomentar cuando sea necesario)
        plt.savefig(f"./siogas_callao/img/tloss_{perfil['latitude'].unique().item()}_{perfil['longitude'].unique().item()}.webp", bbox_inches="tight")
        plt.close("all")
        print(f"Imagen creada_{str(perfil['latitude'].unique().item())}_{str(perfil['longitude'].unique().item())}")
    
    else:
        print(f"Sin datos en {str(puntos_grilla['latitude'][i])}_{str(puntos_grilla['longitude'][i])}")
