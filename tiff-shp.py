import rasterio
from matplotlib import pyplot
from matplotlib import pyplot as plt
import fiona
import rasterio
import rasterio.mask
import numpy as np
import shapefile as shp  # Requires the pyshp package
import skimage

from osgeo import gdal


# Ruta al archivo TIFF original
ruta_geotiff = "/content/drive/MyDrive/conafor/l8_s2.tif"
shp = "/content/drive/MyDrive/conafor/shapes/MC3341_CCL_DISS/MC3341_CCL_DISS.shp"



# Cargar la imagen TIFF original
imagen_original = gdal.Open(ruta_geotiff)

# Obtener la información de georreferenciación
geotransform = imagen_original.GetGeoTransform()
proyeccion = imagen_original.GetProjection()

# Leer la matriz de píxeles
matriz_pixeles_gee = imagen_original.ReadAsArray()
sf = shp.Reader(shp)
sf = shp.Reader(shp)

with fiona.open(shp, "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]



with rasterio.open("/content/drive/MyDrive/conafor/l8_s2.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, invert=False)
    out_meta = src.meta



with rasterio.open("/content/drive/MyDrive/conafor/l8_s2.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, invert=False)


matriz_modificada = np.where(out_image != 0,matriz_pixeles_original ,0)



imagen_original.GetRasterBand(1).ReadAsArray().shape

# Ruta para guardar la nueva imagen TIFF con georreferenciación
ruta_tif_modificado = "/content/drive/MyDrive/conafor/nueva_imagen.tif"


# Crear una nueva imagen en blanco
imagen_modificada = gdal.GetDriverByName('GTiff').Create(
    ruta_tif_modificado, imagen_original.RasterXSize, imagen_original.RasterYSize,imagen_original.RasterCount
    , gdal.GDT_Float64)

# Copiar la información de georreferenciación y proyección a la nueva imagen
imagen_modificada.SetGeoTransform(geotransform)
imagen_modificada.SetProjection(proyeccion)



# Escribir la matriz modificada en la nueva imagen TIFF
for banda in range(1, imagen_original.RasterCount +1):
    imagen_modificada.GetRasterBand(banda).WriteArray(matriz_modificada[banda -1,:,:])  # Cambia 1 al número de banda adecuado si tienes múltiples bandas

# Cerrar los archivos
imagen_original = None
imagen_modificada = None

print("La imagen TIFF modificada con georreferenciación se ha guardado con éxito.")

