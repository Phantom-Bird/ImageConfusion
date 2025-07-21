from confusion import confuse, deconfuse
from PIL import Image
from config import *

img = Image.open('example/image.png')
con_img = confuse(img, (BLOCK_SIZE, BLOCK_SIZE), GRID_WIDTH, RULER_SIZE, DEFAULT_SEED)
con_img.save('example/confused.png')
con_img.resize((img.width // 3, img.height // 3)).save('example/compressed.jpg', optimize=True, quality=30)
con_compressed = Image.open('example/compressed.jpg')
deconfuse(con_compressed, DEFAULT_SEED).save('example/final.jpg')
