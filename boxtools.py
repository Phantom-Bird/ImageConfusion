def box(x1, y1, x2, y2):
    """
    将闭区间 box 转为左闭右开区间 box
    """
    return x1, y1, x2 + 1, y2 + 1
