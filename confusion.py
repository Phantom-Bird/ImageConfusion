import os

from permutation import random_permutations, inverse, apply
from block import *
from boxtools import box
from ruler import add_grid_and_ruler, delete_ruler_and_grid, recognize_ruler
from PIL import Image
from block_shuffle import shuffle_blocks_by
from ruler_fix import fix_ruler


def confuse(img: Image.Image, block_size: tuple[int, int], grid_width: int, ruler_size: int, seed) -> Image.Image:
    """混淆图片并添加标尺"""
    blocks = get_stacked_equal_blocks_of(img.size, block_size)

    px, py = random_permutations((len(blocks.x_blocks), len(blocks.y_blocks)), seed)
    # print(px, py)

    output_img = shuffle_blocks_by(img, blocks, px, py, get_virt_size(block_size, img.size))
    output_img, _ = add_grid_and_ruler(output_img, block_size, grid_width, ruler_size)
    return output_img

def deconfuse(img: Image.Image, seed) -> Image.Image | None:
    """解析标尺解混淆图片"""
    blocks = recognize_ruler(img)
    if blocks is None:
        return None

    print(blocks)
    blocks = BlocksInfo(list(fix_ruler(blocks.x_blocks)),
                        list(fix_ruler(blocks.y_blocks)))
    print(blocks)

    output_img, stacked_blocks = delete_ruler_and_grid(img, blocks)

    px, py = random_permutations((len(blocks.x_blocks), len(blocks.y_blocks)), seed)
    # print(px, py)

    return shuffle_blocks_by(output_img, stacked_blocks, inverse(px), inverse(py))


if __name__ == '__main__':
    _img = Image.open('test.png')
    _con_img = confuse(_img, (16, 16), 4, 16, 0)
    _con_img.show()

    # 测试压缩图像鲁棒性
    _con_img.resize((_img.width // 2, _img.height // 2)).save('test_con.jpg', optimize=True, quality=60)
    _con_img = Image.open('test_con.jpg').copy()  # copy 防止占用图片文件导致清理失败
    os.remove('test_con.jpg')

    _con_img.show()

    _de_img = deconfuse(_con_img, 0)
    _de_img.show()
