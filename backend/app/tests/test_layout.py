"""Unit tests for the standalone layout module — pure geometry, no HTTP."""

import pytest

from app.engines.layout import compute_layout


@pytest.fixture
def corridor_seed():
    """狭长走廊 seed room (8.0 x 1.2) with the 800x800 tile."""
    return dict(room_l=8.0, room_w=1.2, tile_l=0.8, tile_w=0.8)


@pytest.fixture
def square_room():
    """方形小房 3.0 x 3.0 with the 800x800 tile."""
    return dict(room_l=3.0, room_w=3.0, tile_l=0.8, tile_w=0.8)


def test_living_room_6x4_5_with_600_tile():
    layout = compute_layout(6.0, 4.5, 0.6, 0.6)
    assert layout["cols"] == 10
    assert layout["rows"] == 8
    assert layout["grid_count"] == 80
    # length divides evenly; width leaves a 0.3 m cut strip
    assert layout["edge_l"] == pytest.approx(0.6)
    assert layout["edge_w"] == pytest.approx(0.3)


def test_corridor_seed_layout(corridor_seed):
    layout = compute_layout(**corridor_seed)
    assert layout["cols"] == 10
    assert layout["rows"] == 2
    assert layout["grid_count"] == 20
    assert layout["edge_l"] == pytest.approx(0.8)
    assert layout["edge_w"] == pytest.approx(0.4)


def test_square_room_layout(square_room):
    layout = compute_layout(**square_room)
    assert layout["cols"] == 4
    assert layout["rows"] == 4
    assert layout["grid_count"] == 16
    assert layout["edge_l"] == pytest.approx(0.6)
    assert layout["edge_w"] == pytest.approx(0.6)


@pytest.mark.parametrize("tile_l,tile_w", [(0.0, 0.8), (0.8, 0.0), (-0.6, 0.6)])
def test_non_positive_tile_edge_rejected(tile_l, tile_w):
    with pytest.raises(ValueError):
        compute_layout(6.0, 4.5, tile_l, tile_w)
