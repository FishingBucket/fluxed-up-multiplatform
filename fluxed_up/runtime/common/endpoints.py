__all__ = ["Endpoints"]

from dataclasses import dataclass


@dataclass
class Endpoints:
    """
    A dataclass representing all top-level endpoint URLs of a platform.
    """

    http_api: str
    gateway: str
    static_media: str
    user_content: str
    invite: str
    app: list[str]

    def __post_init__(self) -> None:
        self.http_api = self.http_api.rstrip("/")
        self.gateway = self.gateway.rstrip("/")
        self.static_media = self.static_media.rstrip("/")
        self.user_content = self.user_content.rstrip("/")
        self.invite = self.invite.rstrip("/")
        self.app = [url.rstrip("/") for url in self.app]
