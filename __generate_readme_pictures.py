from confusion import confuse, deconfuse
from PIL import Image
from config import *

scaling = 0.2
quality = 20

img = Image.open('example/image.png')
con_img = confuse(img, (BLOCK_SIZE, BLOCK_SIZE), GRID_WIDTH, RULER_SIZE, DEFAULT_SEED)
con_img.save('example/confused.png')
con_img.resize((int(scaling * con_img.width), int(scaling * con_img.height))) \
       .save(f'example/compressed_{scaling}_{quality}.jpg', optimize=True, quality=quality)
con_compressed = Image.open(f'example/compressed_{scaling}_{quality}.jpg')
deconfuse(con_compressed, DEFAULT_SEED).save(f'example/final_{scaling}_{quality}.jpg')
