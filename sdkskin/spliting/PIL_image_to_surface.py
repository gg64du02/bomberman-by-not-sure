# from https://stackoverflow.com/questions/38665920/convert-pil-image-into-pygame-surface-image
from PIL import Image
import pygame
# image = Image.open("SomeImage.png")
image = Image.open("Tile.bmp")


mode = image.mode
size = image.size
data = image.tobytes()

py_image = pygame.image.fromstring(data, size, mode)

print(type(py_image))