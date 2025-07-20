from collections import namedtuple
from collections.abc import Generator
from math import ceil

BlocksInfo = namedtuple('BlocksInfo', ['x_blocks', 'y_blocks'])
Block = tuple[int, int]

def get_stacked_equal_blocks_of(size: tuple[int, int], block_size: tuple[int, int]) -> BlocksInfo:
    """
    获取等大、紧密的分块（注意：传入此块须配合虚拟大小防止截断）
    """

    return BlocksInfo(
        [(i, i + block_size[0] - 1) for i in range(0, size[0], block_size[0])],
        [(i, i + block_size[1] - 1) for i in range(0, size[1], block_size[1])]
    )

def total_size_of(b: list[Block]) -> int:
    """
    计算一个块列表的总大小
    """

    return sum(r - l + 1 for l, r in b)

def __get_stacked_blocks(b: list[Block]) -> Generator[tuple[int, int]]:
    coord = 0
    for i in range(len(b)):
        yield coord, coord + b[i][1] - b[i][0]
        coord += b[i][1] - b[i][0] + 1

def get_stacked_blocks_of(blocks: BlocksInfo) -> BlocksInfo:
    """
    将块信息转换为堆叠块信息。堆叠块之间不留空隙。
    """

    return BlocksInfo(
        list(__get_stacked_blocks(blocks.x_blocks)),
        list(__get_stacked_blocks(blocks.y_blocks))
    )

def get_virt_size(block_size: tuple[int, int], img_size: tuple[int, int]) -> tuple[int, int]:
    """
    获取虚拟图片大小，防止块超出图像范围
    """

    return (block_size[0] * ceil(img_size[0] / block_size[0]),
            block_size[1] * ceil(img_size[1] / block_size[1]))
