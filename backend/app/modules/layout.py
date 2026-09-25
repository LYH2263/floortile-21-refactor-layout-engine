"""铺贴矩形网格布局：行列数、整块数与沿长/沿宽余边长度。

纯几何模块，不依赖 FastAPI 或数据库，可独立 import。
余边长度定义为最后一条裁切带的宽度：room_dim - (units - 1) * tile_dim，
满铺（无裁切）时等于一条完整砖边。
"""

from app.engines.helpers import ceil_units


def compute_layout(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
) -> dict:
    """返回 {cols, rows, grid_count, remainder_l, remainder_w}。

    cols/rows 为沿房间长/宽方向铺设的砖格数（ceil 取整）；
    remainder_l/remainder_w 为对应方向最后一条带的余边长度（米）。
    砖边非正（<=0）时抛 ValueError。
    """
    tl = float(tile_l)
    tw = float(tile_w)
    if tl <= 0 or tw <= 0:
        raise ValueError("tile edge must be positive")

    rl = float(room_l)
    rw = float(room_w)
    cols = ceil_units(rl / tl)
    rows = ceil_units(rw / tw)
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": cols * rows,
        "remainder_l": round(rl - (cols - 1) * tl, 9),
        "remainder_w": round(rw - (rows - 1) * tw, 9),
    }
