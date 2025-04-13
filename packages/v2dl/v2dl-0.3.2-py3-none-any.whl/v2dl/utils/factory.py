from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from logging import Logger
from typing import Any

from .download import (
    ActorDownloadAPI,
    BaseDownloadAPI,
    DirectoryCache,
    ImageDownloadAPI,
    VideoDownloadAPI,
)
from .multitask import AsyncService, BaseTaskService, ThreadingService
from ..common.config import ConfigManager


@dataclass
class Task:
    """Unified task container for both threading and async services."""

    task_id: str
    func: Callable[..., Any]
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        self.kwargs = self.kwargs or {}


class ServiceType(Enum):
    """Service type enumeration."""

    THREADING = "threading"
    ASYNC = "async"
    ACTOR = "actor"


class MediaType(Enum):
    """Media type enumeration."""

    IMAGE = "image"
    VIDEO = "video"


class TaskServiceFactory:
    """Factory class for creating task services."""

    @staticmethod
    def create(
        service_type: ServiceType,
        logger: Logger,
        max_workers: int = 5,
    ) -> BaseTaskService:
        """Create a new task service instance."""
        if service_type == ServiceType.THREADING:
            return ThreadingService(logger, max_workers)
        elif service_type == ServiceType.ASYNC:
            return AsyncService(logger, max_workers)
        else:
            raise ValueError(f"Unknown service type: {service_type}")


class DownloadAPIFactory:
    """Factory for creating download API instances."""

    _api_registry: dict[ServiceType, type[BaseDownloadAPI]] = {
        ServiceType.THREADING: ImageDownloadAPI,
        ServiceType.ASYNC: ImageDownloadAPI,
        ServiceType.ACTOR: ActorDownloadAPI,
    }

    @classmethod
    def create(
        cls,
        service_type: ServiceType,
        headers: dict[str, str],
        rate_limit: int,
        force_download: bool,
        logger: Logger,
        media_type: MediaType = MediaType.IMAGE,
    ) -> BaseDownloadAPI:
        """Create a download API instance based on service type and media type."""
        api_class = cls._api_registry.get(service_type)
        cache = DirectoryCache()
        if not api_class:
            raise ValueError(f"Unknown service type: {service_type}")

        if media_type == MediaType.VIDEO:
            return VideoDownloadAPI(headers, rate_limit, force_download, cache)

        return api_class(headers, rate_limit, force_download, cache)


def create_download_service(
    config_manager: ConfigManager,
    headers: dict[str, str],
    service_type: ServiceType = ServiceType.ASYNC,
) -> tuple[BaseTaskService, Callable[..., Any]]:
    """Create runtime configuration with integrated download service and function."""

    download_service = TaskServiceFactory.create(
        service_type=service_type,
        logger=config_manager.get("static_config", "logger"),
        max_workers=config_manager.get("static_config", "max_worker"),
    )

    download_api = DownloadAPIFactory.create(
        service_type=service_type,
        headers=headers,
        rate_limit=config_manager.get("static_config", "rate_limit"),
        force_download=config_manager.get("static_config", "force_download"),
        logger=config_manager.get("static_config", "logger"),
    )

    download_function = (
        download_api.download_async if service_type == ServiceType.ASYNC else download_api.download
    )
    return download_service, download_function
