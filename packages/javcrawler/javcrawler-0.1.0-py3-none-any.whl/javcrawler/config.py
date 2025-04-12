from dataclasses import dataclass


@dataclass
class _Config:
    url: str
    entries: int
    ua: str
    interval: int
    http_proxy: str | None = None
    https_proxy: str | None = None

    def __post__init__(
        self,
    ):
        self.http_proxy = None
        if self.https_proxy is None:
            self.https_proxy = self.http_proxy


config = _Config(
    url="https://www.javdb.com",
    entries=5,
    ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    interval=3,
    http_proxy="http://localhost:7890",
    https_proxy="http://localhost:7890",
)
