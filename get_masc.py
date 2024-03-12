import rasterio
from matplotlib import pyplot as plt
import fiona
import numpy as np
from osgeo import gdal, osr, ogr,gdalconst
import geopandas as gpd
import random
from shapely.geometry import Point

ruta_shapefile = "file.shp"
ruta_tif =  "image.tif"


imagen_tif = gdal.Open(ruta_tif, gdalconst.GA_Update)
if imagen_tif is not None:
  print("Imagen abierta correctamente")

# Leer la matriz de píxeles
matriz_pixeles = imagen_tif.ReadAsArray()
mascara_id = np.zeros(matriz_pixeles.shape[-2:])

# Define las propiedades de la nueva banda
tipo_dato = gdal.GDT_Float32  # Tipo de datos de la nueva banda (puedes cambiarlo según tus necesidades)
num_bandas = imagen_tif.RasterCount  # Obtiene el número de bandas en la imagen existente

# Crea la nueva banda vacía
nueva_banda = imagen_tif.GetRasterBand(num_bandas + 1)  # Asigna un número de banda único
geotransform = imagen_tif.GetGeoTransform()
proyeccion = imagen_tif.GetProjection()


# Abrir shapefile
shapefile = ogr.Open(ruta_shapefile)
capa = shapefile.GetLayer(0)
banda = imagen_tif.GetRasterBand(1)



poligono_lyr = shapefile.GetLayer(0)
geom = capa.GetFeature(0)
poligono_geom = geom.GetGeometryRef()
capa.GetSpatialRef()

imagen_srs = imagen_tif.GetProjection()
poligono_srs = capa.GetSpatialRef()

if imagen_srs == poligono_srs.ExportToWkt():
    print("Los SRS son compatibles.")
else:
    print("Los SRS no son compatibles.")

def get_pixeles(submatrix, ID):
  masc = (submatrix != 0)
  id = np.zeros(submatrix.shape)
  id[masc] = ID
  return id

def change_masc_tiff(id_matrix,matriz_original,x,y,xs,ys):
  matriz_original[y:y+ys+1,x:x+xs+1] = id_matrix
  return matriz_original

imagen_srs = osr.SpatialReference(imagen_tif.GetProjection())

# Obtén el sistema de referencia espacial (SRS) del polígono
poligono_srs = poligono_lyr.GetSpatialRef()

# Elige el polígono que deseas procesar (en este ejemplo, el primer polígono)
poligono_feature = poligono_lyr.GetFeature(1)

# Obtiene la geometría del polígono
poligono_geom = poligono_feature.GetGeometryRef()
atributos = poligono_feature.items()

ID = int(atributos['SAMOF_2020'])
print(poligono_geom)
#print(atributos)

transform = osr.CoordinateTransformation(poligono_srs, imagen_srs)
poligono_geom.Transform(transform)

# Obtén el envelope (límites) del polígono en su propio sistema de coordenadas
x_min, x_max, y_min, y_max = poligono_geom.GetEnvelope()


poligono_srs = poligono_lyr.GetSpatialRef()
for i,j in enumerate(poligono_lyr):

    # Elige el polígono que deseas procesar (en este ejemplo, el primer polígono)
    poligono_feature = poligono_lyr.GetFeature(i)

    # Obtiene la geometría del polígono
    poligono_geom = poligono_feature.GetGeometryRef()
    atributos = poligono_feature.items()

    ID = int(atributos['SAMOF_2020'])


    transform = osr.CoordinateTransformation(poligono_srs, imagen_srs)
    poligono_geom.Transform(transform)

    x_min, x_max, y_min, y_max = poligono_geom.GetEnvelope()

    x_min, y_min, _ = transform.TransformPoint(x_min, y_min)
    x_max, y_max, _ = transform.TransformPoint(x_max, y_max)


    banda = imagen_tif.GetRasterBand(1)
    geotransform = imagen_tif.GetGeoTransform()  # Get the geotransform once

    x_off = int((x_min - geotransform[0]) / geotransform[1])
    y_off = int((y_max - geotransform[3]) / geotransform[5])
    x_size = int((x_max - x_min) / geotransform[1])
    y_size = int((y_max - y_min) / abs(geotransform[5]))

    data = banda.ReadAsArray(x_off, y_off, x_size+1, y_size+1)


    mascara_id = change_masc_tiff(get_pixeles(data, atributos['SAMOF_2020']),mascara_id,x_off,y_off,x_size,y_size)




# Save the masked raster to a new file
masked_raster_path = '/content/drive/MyDrive/conafor/masked_raster.tif'
with rasterio.open(masked_raster_path, "w", **out_meta) as dest:
    dest.write(out_image)

