"""fastapi_template package."""
from fastapi_template.pkg.models.core import Containers

__all__ = ["__containers__"]

__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        # Container(container=Services),
    ],
)
