"""Per-IP rate limiting via slowapi.

In-memory storage — fine for single-process dev / small portfolio deploys.
For multi-instance prod, set storage_uri to a Redis URL.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],      # opt-in per endpoint, no global cap
    headers_enabled=False,  # requires `response: Response` param on every route; off for simplicity
)
