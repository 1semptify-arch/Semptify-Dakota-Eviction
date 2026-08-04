"""Minimal ZIP bundle service for the defense packet endpoint."""
import io
import zipfile
from typing import Any, Dict, List


def create_defense_packet_zip(
    documents: List[Dict[str, Any]],
    forms: List[Dict[str, Any]],
    case_info: Dict[str, Any],
    include_instructions: bool = True
) -> bytes:
    """Create a ZIP archive containing defense documents."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, doc in enumerate(documents, 1):
            content = doc.get("content", b"")
            if isinstance(content, str):
                content = content.encode("utf-8")
            zf.writestr(f"{i:02d}_{doc.get('filename', 'document.pdf')}", content)

        if include_instructions:
            zf.writestr(
                "README.txt",
                "Defense packet\n\n"
                "1. Review every document for accuracy.\n"
                "2. Sign and date where indicated.\n"
                "3. File with the court and serve copies as required.\n".encode("utf-8"),
            )

    return buf.getvalue()
