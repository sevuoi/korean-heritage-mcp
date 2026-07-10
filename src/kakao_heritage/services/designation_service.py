from __future__ import annotations


def normalize_designation_type(designation_type: str | None) -> str | None:
    if not designation_type:
        return None
    normalized = designation_type.strip()
    mapping = {
        "국가민속문화재": "국가민속문화유산",
        "문화재": "문화재",
        "천기": "천연기념물",
    }
    return mapping.get(normalized, normalized)
