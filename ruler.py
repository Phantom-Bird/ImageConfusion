"""
ruler 是这个算法的核心。
通过添加 ruler，可以防止图像传输过程中的失真导致的块漂移问题。
"""

from block import *
from PIL import Image
from boxtools import box
import config as cfg


# 以下为编码

def add_grid(img: Image.Image, info: BlocksInfo, grid_width: int, ruler_size: int, virt_size = None) -> tuple[Image.Image, BlocksInfo]:
    """
    为原图添加网格，网格上的像素将会顺延。返回添加网格后的 Image, BlocksInfo
    :param img: 原图
    :param info: 原图的 BlocksInfo
    :param grid_width: 网格宽度
    :param ruler_size: 为标尺预留的宽度
    :param virt_size: 虚拟尺寸，如果为 None，则使用原图尺寸
    """

    if virt_size is None:
        virt_size = img.size

    output_size = (virt_size[0] + ruler_size + grid_width * (len(info.x_blocks) - 1),
                   virt_size[1] + ruler_size + grid_width * (len(info.y_blocks) - 1))
    output_img = Image.new("RGB", output_size, (0, 0, 0))

    output_info = BlocksInfo([], [])

    for ix, (x1, x2) in enumerate(info.x_blocks):
        output_info.x_blocks.append((x1 + ruler_size + grid_width * ix,
                                     x2 + ruler_size + grid_width * ix))

    for iy, (y1, y2) in enumerate(info.y_blocks):
        output_info.y_blocks.append((y1 + ruler_size + grid_width * iy,
                                     y2 + ruler_size + grid_width * iy))

    for (x1, x2), (x1_new, x2_new) in zip(info.x_blocks, output_info.x_blocks):
        for (y1, y2), (y1_new, y2_new) in zip(info.y_blocks, output_info.y_blocks):
            output_img.paste(img.crop(box(x1, y1, x2, y2)), box(x1_new, y1_new, x2_new, y2_new))

    return output_img, output_info


def add_ruler(img: Image, info: BlocksInfo, ruler_size: int) -> None:
    """
    绘制标尺，即在图片上/左方的 Block 坐标上绘制白块。
    **请注意：这是原地的**
    :param img: 待绘制图片
    :param info: 块信息
    :param ruler_size: 标尺大小
    """

    for x1, x2 in info.x_blocks:
        img.paste((255, 255, 255), box(x1, 0, x2, ruler_size - 1))

    for y1, y2 in info.y_blocks:
        img.paste((255, 255, 255), box(0, y1, ruler_size - 1, y2))
        
def fill_gaps(img: Image.Image, blocks: BlocksInfo):
    """
    原地将块间空隙填充为最近邻像素
    """
    
    for (_, pre_x2), (next_x1, _) in zip(blocks.x_blocks, blocks.x_blocks[1:]):
        mid = (pre_x2 + next_x1) // 2
        
        left_crop = img.crop(box(pre_x2, 0, pre_x2, img.height - 1))
        for x in range(pre_x2 + 1, mid + 1):
            img.paste(left_crop, (x, 0))
            
        right_crop = img.crop(box(next_x1, 0, next_x1, img.height - 1))
        for x in range(mid + 1, next_x1):
            img.paste(right_crop, (x, 0))
            
    for (_, pre_y2), (next_y1, _) in zip(blocks.y_blocks, blocks.y_blocks[1:]):
        mid = (pre_y2 + next_y1) // 2
        
        up_crop = img.crop(box(0, pre_y2, img.width - 1, pre_y2))
        for y in range(pre_y2 + 1, mid + 1):
            img.paste(up_crop, (0, y))
            
        down_crop = img.crop(box(0, next_y1, img.width - 1, next_y1))
        for y in range(mid + 1, next_y1):
            img.paste(down_crop, (0, y))

def add_grid_and_ruler(img: Image.Image, block_size: tuple[int, int], grid_width: int, ruler_size: int) -> tuple[Image.Image, BlocksInfo]:
    info = get_stacked_equal_blocks_of(img.size, block_size)
    virt_size = get_virt_size(block_size, img.size)

    output_img, output_info = add_grid(img, info, grid_width, ruler_size, virt_size)
    # print(output_info)
    fill_gaps(output_img, output_info)
    add_ruler(output_img, output_info, ruler_size)
    return output_img, output_info
        

# 以下为解码

BLACK = 0
WHITE = 1
NONE  = 2

def color2wb(color):
    if all(channel >= cfg.WHITE_THRESHOLD for channel in color):
        return WHITE
    elif all(channel <= cfg.BLACK_THRESHOLD for channel in color):
        return BLACK
    return NONE

def recognize_ruler(img: Image.Image) -> BlocksInfo | None:
    img.convert('RGB')

    if color2wb(img.getpixel((0, 0))) != BLACK:
        return None

    x_blocks = []
    pre_wb = BLACK
    for x in range(img.width):
        white_black = color2wb(img.getpixel((x, 0)))
        if white_black == NONE or white_black == pre_wb:
            continue

        if white_black == WHITE:
            x_blocks.append((x, 0))
        else:
            x_blocks[-1] = (x_blocks[-1][0], x - 1)

        pre_wb = white_black

    if not x_blocks:
        return None
    if x_blocks[-1][1] == 0:
        x_blocks[-1] = (x_blocks[-1][0], img.width - 1)

    y_blocks = []
    pre_wb = BLACK
    for y in range(img.height):
        white_black = color2wb(img.getpixel((0, y)))
        if white_black == NONE or white_black == pre_wb:
            continue

        if white_black == WHITE:
            y_blocks.append((y, 0))
        else:
            y_blocks[-1] = (y_blocks[-1][0], y - 1)

        pre_wb = white_black

    if not y_blocks:
        return None
    if y_blocks[-1][1] == 0:
        y_blocks[-1] = (y_blocks[-1][0], img.height - 1)

    return BlocksInfo(x_blocks, y_blocks)

def delete_ruler_and_grid(img: Image.Image, info: BlocksInfo) -> tuple[Image.Image, BlocksInfo]:
    """
    将含有标尺和网格的图片转换为正常图片
    :param img: 原图
    :param info: 原图的 BlockInfo
    :return: (转换后的图片, 转换后的 BlockInfo)
    """

    output_size = (total_size_of(info.x_blocks), total_size_of(info.y_blocks))
    output_img = Image.new('RGB', output_size, (255, 255, 255))
    stacked_blocks = get_stacked_blocks_of(info)
    x_stack, y_stack = stacked_blocks

    for (x1, x2), (x_coord, _) in zip(info.x_blocks, x_stack):
        for (y1, y2), (y_coord, _) in zip(info.y_blocks, y_stack):
            output_img.paste(img.crop(box(x1, y1, x2, y2)), (x_coord, y_coord))
            # +1 是因为 Image.crop 的坐标是左闭右开的

    return output_img, stacked_blocks

if __name__ == '__main__':
    img = Image.open('test.png')
    output_img, new_info = add_grid_and_ruler(img, (12, 12), 2, 20)
    output_img.show()

    recognize_info = recognize_ruler(output_img)

    if recognize_info is None:
        print('未检测到标尺')

    img, blocks = delete_ruler_and_grid(output_img, recognize_info)
    img.show()
    print(blocks)
