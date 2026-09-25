"""Floor tile order count: area method, with layout sourced from app.engines.layout."""

from app.engines.helpers import ceil_units
from app.engines.layout import compute_layout


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    order_count: ceil(raw * (1 + waste_pct/100))
    layout: delegated wholesale to the standalone layout module
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    with_waste = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    geometry = compute_layout(room_l, room_w, tile_l, tile_w)
    # External JSON keeps its original keys; edge strip lengths stay module-level.
    layout = {
        "cols": geometry["cols"],
        "rows": geometry["rows"],
        "grid_count": geometry["grid_count"],
    }
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "order_count": with_waste,
        "layout": layout,
    }


# Backward-compatible facade: geometry lives in app.engines.layout.
def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    geometry = compute_layout(room_l, room_w, tile_l, tile_w)
    return {
        "cols": geometry["cols"],
        "rows": geometry["rows"],
        "grid_count": geometry["grid_count"],
    }
