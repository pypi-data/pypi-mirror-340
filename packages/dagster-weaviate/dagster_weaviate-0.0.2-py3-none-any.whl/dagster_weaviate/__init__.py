from dagster._core.libraries import DagsterLibraryRegistry

from dagster_weaviate.resource import (
    WeaviateResource as WeaviateResource,
)

from dagster_weaviate.config import (
    LocalConfig as LocalConfig,
    CloudConfig as CloudConfig,
)

__version__ = "0.0.2"

DagsterLibraryRegistry.register("dagster-weaviate", __version__)
