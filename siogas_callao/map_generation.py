
"""
# Coordenadas a eliminar (lat, lon)
coordenadas_a_eliminar = [(-17.25, -71.5), (-18.25, -70.5), (-16.5,-73), (-16.25,-73.5), (-16,-74), (-15.25,-75.25), (-14.75,-75.15), 
                          (-12.5,-76.75), (-10.75,-77.75), (-9.75,-78.25), (-8.75,-78.75), (1.25,-79.25), (-7.25,-79.75),
                          (-14.75 , -75.75), (-22.5,-70.25), (-26.75,-69.75), (-38.25,-73.5), (-38.5,-73.5), (-44.5,-74.5),
                          (-44.75,-74.5), (-53,74.5), (-53.75,-71.75), (-55,-71.25)]
# Filtramos las filas que NO están en la lista de coordenadas a eliminar
coordenadas = coordenadas[~coordenadas.apply(lambda row: (row['latitude'], row['longitude']) in coordenadas_a_eliminar, axis=1)].reset_index(drop=True)
"""

import folium
import os
import re
from pathlib import Path
import os
os.chdir(os.getcwd())

# Configuración
img_folder = Path("img/")  # Usamos Path para mejor manejo de rutas
m = folium.Map(location=[-12, -79.5], zoom_start=5)
transmision_loss = folium.FeatureGroup(name="Propagación", show=True).add_to(m)

# Regex optimizado para tus nombres de archivo
pattern = re.compile(r'tloss_(-?\d+\.\d+)_(-?\d+\.\d+)\.webp$')

# Contadores para diagnóstico
total_imgs = 0
markers_creados = 0

for img_file in img_folder.glob('tloss_*_*.webp'):
    match = pattern.match(img_file.name)
    if not match:
        continue
        
    total_imgs += 1
    
    try:
        lat = float(match.group(1))
        lon = float(match.group(2))
        
        # Construir ruta relativa para el popup
        img_path = img_folder.name + '/' + img_file.name
        html = f'<img src="{img_path}" width="800" height="400">'
        
        folium.CircleMarker(
            location=[lat, lon],
            popup=html,
            radius=5,
            color='black',
            fill=True,
            fill_color= 'black',
            fill_opacity=0.7
        ).add_to(transmision_loss)
        markers_creados += 1
        
    except (ValueError, TypeError) as e:
        print(f"Error procesando {img_file.name}: {str(e)}")

# Estadísticas
print(f"\nResumen:")
print(f"• Imágenes encontradas: {total_imgs}")
print(f"• Markers creados: {markers_creados}")
print(f"• Procesamiento completado")

# Guardar mapa
m.save("mapa_automatico.html")
print("Mapa guardado como 'mapa_automatico.html'")
