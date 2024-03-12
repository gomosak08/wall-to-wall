from osgeo import gdal
import numpy as np



path = 'image_path.tif'
mascara = np.load('mascara.npy')
imagen_tif = gdal.Open(path)
matriz_pixeles = imagen_tif.ReadAsArray()




def divide_image_np(image, rows, cols):
    """
    Divides an image into a specified number of rows and columns.

    Args:
    - image: A NumPy array representing the image.
    - rows: The number of rows to divide the image into.
    - cols: The number of columns to divide the image into.

    Returns:
    - A list of NumPy arrays, each representing a sub-image.
    """
    h, w = image[0].shape
    return np.array([image[:,h//rows*row:h//rows*(row+1), w//cols*col:w//cols*(col+1)] for row in range(rows) for col in range(cols)])


def divide_image_masks(image, rows, cols):
    """
    Divides an image into a specified number of rows and columns.

    Args:
    - image: A NumPy array representing the image.
    - rows: The number of rows to divide the image into.
    - cols: The number of columns to divide the image into.

    Returns:
    - A list of NumPy arrays, each representing a sub-image.
    """
    h, w = image.shape
    return np.array([image[h//rows*row:h//rows*(row+1), w//cols*col:w//cols*(col+1)] for row in range(rows) for col in range(cols)])

# changing the clases range
mascara[mascara == -5] = 0
mascara[mascara == 2] = 1
mascara[mascara == 3] = 1
mascara[mascara == 6] = 1
mascara[mascara == 12] = 1
mascara[mascara == 12] = 1
mascara[mascara == 28] = 3
mascara[mascara == 29] = 2
mascara[mascara == 30] = 5
mascara[mascara == 31] = 6
mascara[mascara == 32] = 4
mascara[mascara == 280] = 3

# dividing the image in the specific numer of row and colummns 
images = divide_image_np(matriz,6,6)
mascara_img =  divide_image_masks(mascara,6,6)


#taking the images that are not empty and saving
for i,j in enumerate(mascara_img):
  if not np.all(j == 0):
    array = j.astype(np.float32) 
    np.save(f'masks/{i}.npy', array)

    img = images[i]
    img = img.astype(np.float32)
    np.save(f'data/{i}.npy', img)
