# 模块作单例模式
from unittest.mock import DEFAULT

BLOCK_SIZE = 16
GRID_WIDTH = 4
RULER_SIZE = 32

BLACK_THRESHOLD = 127
WHITE_THRESHOLD = 128

assert BLACK_THRESHOLD < WHITE_THRESHOLD, "Black threshold should be less than white threshold"

# 仅 GUI，只读
IMG_VIEW_SIZE = (256, 256)
DEFAULT_COLOR = (63, 63, 63)
DEFAULT_SEED = 'DEFAULT_SEED'
