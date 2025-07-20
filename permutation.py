import random
from collections.abc import Generator


def random_permutations(lengths: tuple[int, ...], seed) -> Generator[list[int]]:
    """
    按照 seed 生成一个长度为 n 的随机排列
    :returns: 排列, 新种子
    """
    random.seed(seed)
    for n in lengths:
        yield random.sample(range(n), n)

def inverse(permutation: list[int]):
    """
    生成一个排列的逆排列
    """
    inv = [None] * len(permutation)
    for i, p in enumerate(permutation):
        inv[p] = i

    return inv

def apply(permutation, sequence: list):
    """
    将排列应用到序列上
    """
    return [sequence[p] for p in permutation]
