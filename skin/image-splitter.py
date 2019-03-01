from PIL import Image, ImageFilter
print("lol1")
# check
# https://python-guide-pt-br.readthedocs.io/fr/latest/scenarios/imaging.html
#Read image
im = Image.open( 'Tile.bmp' )
#Display image
im.show()

# #Applying a filter to the image
# im_sharp = im.filter( ImageFilter.SHARPEN )
#Saving the filtered image to a new file
# im_sharp.save( 'Tile2.bmp', 'BMP' )
im.save( 'Tile2.bmp', 'BMP' )
print("lol2")

#Splitting the image into its respective bands, i.e. Red, Green,
#and Blue for RGB
# r,g,b = im_sharp.split()

#Viewing EXIF data embedded in image
# exif_data = im._getexif()
# exif_data
i = 0
width = 32
height = 32
for i in range(256):
    im2 = im
    x= i%16
    y= int(i/16)
    print("(x,y)",x,y)
    box = (32*x, 32*y, 32*x+width, 32*y+height)
    a = im2.crop(box)
    # a.show()
    a.save('tile_' + str(x) + '_' + str(y) + '.bmp', 'BMP')