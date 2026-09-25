"""Rectangular tile laying layout.

All lattice geometry lives here so engines/services never inline rows/columns
arithmetic: column/row counts, grid block count and the cut-tile strip lengths
left along the room's long (``l``) and short (``w``) edges.
"""

from app.engines.helpers import ceil_units


def compute_layout(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
) -> dict:
    """Lay tiles on a full rectangular lattice.

    ``cols`` tiles run along the room length, ``rows`` along the width.
    ``edge_l``/``edge_w`` are the strip lengths of the last (possibly cut)
    tile column/row; they equal the tile edge when the room divides evenly.

    Raises ValueError when a room or tile edge is not strictly positive.
    """
    room_l, room_w = float(room_l), float(room_w)
    tile_l, tile_w = float(tile_l), float(tile_w)
    if room_l <= 0 or room_w <= 0:
        raise ValueError("room dimensions must be positive")
    if tile_l <= 0 or tile_w <= 0:
        raise ValueError("tile edges must be positive")

    cols = ceil_units(room_l / tile_l)
    rows = ceil_units(room_w / tile_w)
    edge_l = room_l - (cols - 1) * tile_l
    edge_w = room_w - (rows - 1) * tile_w
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": cols * rows,
        "edge_l": round(edge_l, 6),
        "edge_w": round(edge_w, 6),
    }
