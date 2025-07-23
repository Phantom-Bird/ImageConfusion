from confusion import confuse, deconfuse
from PIL import Image
from config import *

scaling = 0.5
quality = 50

img = Image.open('example/image.png')
con_img = confuse(img, (BLOCK_SIZE, BLOCK_SIZE), GRID_WIDTH, RULER_SIZE, DEFAULT_SEED)
con_img.save('example/confused.png')
con_img.resize((int(scaling * con_img.width), int(scaling * con_img.height))) \
       .save('example/compressed.jpg', optimize=True, quality=quality)
con_compressed = Image.open('example/compressed.jpg')
deconfuse(con_compressed, DEFAULT_SEED).save('example/final.jpg')
