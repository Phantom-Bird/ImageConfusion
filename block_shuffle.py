from PIL import Image
from boxtools import box
from permutation import inverse, apply
from block import *

def shuffle_blocks(img: Image.Image, blocks_old: BlocksInfo, blocks_new: BlocksInfo, virt_size: tuple[int, int] | None = None):
    """
    将 img 中的 x_blocks 按照 blocks_old -> blocks_new 重新排列
    """

    if virt_size is None:
        virt_size = img.size

    output_img = Image.new('RGB', virt_size, (255, 255, 255))

    for (x1_old, x2_old), (x1_new, x2_new) in zip(blocks_old.x_blocks, blocks_new.x_blocks):
        for (y1_old, y2_old), (y1_new, y2_new) in zip(blocks_old.y_blocks, blocks_new.y_blocks):
            output_img.paste(img
                                 .crop(box(x1_old, y1_old, x2_old, y2_old))
                                 .resize((x2_new - x1_new + 1, y2_new - y1_new + 1)),
                             box(x1_new, y1_new, x2_new, y2_new))

    return output_img

def shuffle_blocks_by(img: Image.Image, blocks_old: BlocksInfo, permutation_x: list[int], permutation_y: list[int], virt_size: tuple[int, int] | None = None):
    """
    将 img 中的 x_blocks 按照 permutation_x 和 permutation_y 重新排列
    :param img: 原图片
    :param blocks_old: 原图片的块信息
    :param permutation_x: x 方向的排列
    :param permutation_y: y 方向的排列
    :param virt_size: 虚拟图片大小（防止块因为图片大小截断），为 None 则使用原图片大小
    """
    blocks_new = BlocksInfo(
        apply(permutation_x, blocks_old.x_blocks),
        apply(permutation_y, blocks_old.y_blocks))
    return shuffle_blocks(img, blocks_old, blocks_new, virt_size)

if __name__ == '__main__':
    img = Image.open('test.png')
    blocks = BlocksInfo([(0, 200), (201, 600)], [(0, 200), (201, 400)])
    px = py = [1, 0]
    output_img = shuffle_blocks_by(img, blocks, px, py)
    output_img.show()

    shuffle_blocks_by(output_img, blocks, inverse(px), inverse(py)).show()
