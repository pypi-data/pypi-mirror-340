"""
WebTransport implementation for Python.

A library for WebTransport over HTTP/3 implementation using the aioquic library.
"""

__version__ = "0.0.1"

# Public API
from .handlers.base import WebTransportHandler
from .handlers.counter import CounterHandler
from .handlers.echo import EchoHandler
from .protocols.http3 import WebTransportProtocol
from .server import start_server

__all__ = [
    "start_server",
    "WebTransportHandler",
    "CounterHandler",
    "EchoHandler",
    "WebTransportProtocol",
]
