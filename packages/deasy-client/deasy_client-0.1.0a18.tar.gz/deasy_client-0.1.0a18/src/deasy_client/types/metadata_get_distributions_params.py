# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["MetadataGetDistributionsParams"]


class MetadataGetDistributionsParams(TypedDict, total=False):
    analysis_level: Required[str]

    vdb_profile_name: Required[str]

    schema_names: Optional[List[str]]

    tag_names: Optional[List[str]]
