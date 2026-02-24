
from typing import Optional
import os

from urllib3.util.retry import Retry
from urllib3 import PoolManager

from . import Configuration, ApiClient
from .api.v1_api import V1Api

__version__ = "1.0.0"


class PulsePointLiveRampClient:
    """
    Production-safe wrapper around the generated V1Api client.

    Features:
    - Environment variable support
    - Default timeout
    - Automatic retries with backoff
    - Header injection
    - Custom User-Agent
    """

    def __init__(
        self,
        host: Optional[str] = None,
        org_id: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30,
        retries: int = 3,
    ):
        host = host or os.getenv("PULSEPOINT_LIVERAMP_HOST")
        org_id = org_id or os.getenv("PULSEPOINT_LIVERAMP_ORG_ID")

        if not host:
            raise ValueError(
                "host must be provided or set via PULSEPOINT_LIVERAMP_HOST"
            )

        if not org_id:
            raise ValueError(
                "org_id must be provided or set via PULSEPOINT_LIVERAMP_ORG_ID"
            )

        config = Configuration(host=host)
        api_client = ApiClient(config)

        # Inject required headers
        api_client.default_headers["X-LR-Org-Id"] = org_id
        api_client.default_headers["User-Agent"] = (
            f"pulsepoint-liveramp-sdk/{__version__}"
        )

        if api_key:
            api_client.default_headers["x-api-key"] = api_key

        # Configure retry strategy
        retry_strategy = Retry(
            total=retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )

        api_client.rest_client.pool_manager = PoolManager(
            retries=retry_strategy,
        )

        # Set default timeout
        api_client.rest_client.pool_manager.connection_pool_kw["timeout"] = timeout

        self._client = V1Api(api_client)

    # ---- Pass-through methods ---- #

    def list_destinations(self, **kwargs):
        return self._client.list_destinations(**kwargs)

    def list_first_party_segments(self, **kwargs):
        return self._client.list_first_party_segments(**kwargs)

    def list_marketplace_segments(self, **kwargs):
        return self._client.list_marketplace_segments(**kwargs)

    def get_marketplace_segment_detail(self, **kwargs):
        return self._client.get_marketplace_segment_detail(**kwargs)

    def request_segments(self, **kwargs):
        return self._client.request_segments(**kwargs)

    def get_segment_statuses(self, **kwargs):
        return self._client.get_segment_statuses(**kwargs)

    def list_deliveries(self, **kwargs):
        return self._client.list_deliveries(**kwargs)

    def health(self):
        return self._client.health()

    def ready(self):
        return self._client.ready()
