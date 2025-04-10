from typing import Any, TypedDict
from dahua.exceptions import DahuaRequestError, DahuaMethodNotSupported


class ListMethodResponse(TypedDict):
    method: list[str]


class RPC:
    def __init__(self, client: "DahuaRpc", parent: str):
        self.client = client
        self.parent = parent

    def _send(self, function: str, **kwargs) -> dict[str, Any]:
        """Send a request to the camera."""
        return self.client._request(method=f"{self.parent}.{function}", **kwargs)

    # ========================================
    # Common Methods
    # ========================================

    def list_method(self) -> ListMethodResponse:
        """Lists all methods of RPC function"""
        try:
            return self._send(function="listMethod").get("params")
        except DahuaRequestError as e:
            raise DahuaMethodNotSupported from e
