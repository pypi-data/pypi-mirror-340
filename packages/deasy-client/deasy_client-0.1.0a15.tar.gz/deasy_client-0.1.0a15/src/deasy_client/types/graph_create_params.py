# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

__all__ = ["GraphCreateParams"]


class GraphCreateParams(TypedDict, total=False):
    graph_name: Required[str]

    graph_data: Optional[Dict[str, object]]

    graph_description: Optional[str]
