from __future__ import annotations

from api.services.integrations.base import IntegrationPackageSpec
from api.services.integrations.registry import register_package

from .node import NODES

PACKAGE = register_package(
    IntegrationPackageSpec(
        name="sales_os",
        nodes=NODES,
    )
)

__all__ = ["PACKAGE"]
