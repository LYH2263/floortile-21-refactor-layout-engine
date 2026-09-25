"""布局模块纯几何测例：直接 import compute_layout，不打 HTTP。"""

import pytest

from app.modules.layout import compute_layout


def test_guest_room_6x45_600():
    """客餐厅 6×4.5 配 0.6×0.6：10 列 × 8 行 = 80 格。"""
    layout = compute_layout(6.0, 4.5, 0.6, 0.6)
    assert layout["cols"] == 10
    assert layout["rows"] == 8
    assert layout["grid_count"] == 80
    # 长向满铺，余边为一整砖；宽向最后一条带 0.3m
    assert layout["remainder_l"] == pytest.approx(0.6)
    assert layout["remainder_w"] == pytest.approx(0.3)


def test_corridor_seed_8x12_800():
    """狭长走廊种子 8×1.2 配 0.8×0.8：10 列 × 2 行 = 20 格。"""
    layout = compute_layout(8.0, 1.2, 0.8, 0.8)
    assert layout["cols"] == 10
    assert layout["rows"] == 2
    assert layout["grid_count"] == 20
    assert layout["remainder_l"] == pytest.approx(0.8)
    assert layout["remainder_w"] == pytest.approx(0.4)


def test_square_small_room_25x25_600():
    """方形小房 2.5×2.5 配 0.6×0.6：5 × 5 = 25 格，两向余边各 0.1m。"""
    layout = compute_layout(2.5, 2.5, 0.6, 0.6)
    assert layout["cols"] == 5
    assert layout["rows"] == 5
    assert layout["grid_count"] == 25
    assert layout["remainder_l"] == pytest.approx(0.1)
    assert layout["remainder_w"] == pytest.approx(0.1)


@pytest.mark.parametrize("tile_l,tile_w", [(0.0, 0.6), (0.6, 0.0), (-0.6, 0.6), (0.6, -0.6)])
def test_reject_non_positive_tile_edge(tile_l, tile_w):
    """砖边为零或为负时拒绝。"""
    with pytest.raises(ValueError):
        compute_layout(6.0, 4.5, tile_l, tile_w)
