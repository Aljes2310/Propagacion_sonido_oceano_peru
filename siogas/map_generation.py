import folium
import base64
import pandas as pd
coordenadas=pd.read_csv("/home/user03/siogas/data/Puntos_grilla.csv")

# Coordenadas a eliminar (lat, lon)
coordenadas_a_eliminar = [(-17.25, -71.5), (-18.25, -70.5), (-16.5,-73), (-16.25,-73.5), (-16,-74), (-15.25,-75.25), (-14.75,-75.15), 
                          (-12.5,-76.75), (-10.75,-77.75), (-9.75,-78.25), (-8.75,-78.75), (1.25,-79.25), (-7.25,-79.75),
                          (-14.75 , -75.75), (-22.5,-70.25), (-26.75,-69.75), (-38.25,-73.5), (-38.5,-73.5), (-44.5,-74.5),
                          (-44.75,-74.5), (-53,74.5), (-53.75,-71.75), (-55,-71.25)]
# Filtramos las filas que NO están en la lista de coordenadas a eliminar
coordenadas = coordenadas[~coordenadas.apply(lambda row: (row['latitude'], row['longitude']) in coordenadas_a_eliminar, axis=1)].reset_index(drop=True)


m = folium.Map(location=[-12,-79.5], zoom_start=5)

#sounds_profiles = folium.FeatureGroup(name="Perfiles", show=True).add_to(m)
transmision_loss = folium.FeatureGroup(name="Propagacion", show=True).add_to(m)

files=[]

import os
import pathlib


for i in range(0,len(coordenadas),1):


    """
    # sounds profiles
    try:
        file=f"Sound_Profile_{coordenadas["latitude"][i]}_{coordenadas["longitude"][i]}.png"
        # 1. Codificar la imagen a Base64
        with open(f"img/join/{file}", "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

        html = f'<img src="data:image/png;base64,{img_base64}" width="300">'

        folium.CircleMarker(location=[coordenadas["latitude"][i],coordenadas["longitude"][i]], fill=True, popup=html,
                                weight=1, fill_opacity=0.7, radius=4, color="black").add_to(sounds_profiles)
    
    except Exception as e:
        print(e)
    """

    # transmission loss
    try :
        file=f"tloss_{coordenadas['latitude'][i]}_{coordenadas['longitude'][i]}.webp"
        # 1. Codificar la imagen a Base64
        #with open(f"img/join/{file}", "rb") as img_file:
         #   img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

        #html = f'<img src="data:image/png;base64,{img_base64}" width="800" height="400">'
        html = f'<img src="img/join/{file}" width="800" height="400">'

        folium.CircleMarker(location=[coordenadas['latitude'][i],coordenadas['longitude'][i]], fill=True, popup=html,
                            weight=1, fill_opacity=0.7, radius=4, color="black").add_to(transmision_loss)
    except Exception as e:
        print(e)



folium.LayerControl().add_to(m)
m.save("mymap.html")
