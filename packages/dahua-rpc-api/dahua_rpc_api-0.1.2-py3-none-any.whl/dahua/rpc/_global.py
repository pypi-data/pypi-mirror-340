from typing import TypedDict
from dahua.rpc import RPC


class LoginParams(TypedDict):
    """Parameters for login."""

    userName: str
    password: str
    clientType: str
    authorityType: str
    passwordType: str


class GlobalRPC(RPC):
    def __init__(self, client: "DahuaRpc") -> None:
        super().__init__(client=client, parent="global")

    def login(self, params: LoginParams, **kwargs) -> dict:
        """Get the software version of the MagicBox."""
        return self._send(
            function="login", endpoint="RPC2_Login", params=params, **kwargs
        )

    def logout(self) -> None:
        self._send(function="logout")
