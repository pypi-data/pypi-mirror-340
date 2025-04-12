"""
WebTransport over HTTP/3 protocol implementation.
"""

import logging
from typing import Dict, Optional, Type

from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.h3.connection import H3Connection
from aioquic.h3.events import H3Event, HeadersReceived
from aioquic.quic.events import ProtocolNegotiated, QuicEvent, StreamReset

# We're importing from parent module to avoid circular imports
from ..handlers.base import WebTransportHandler

logger = logging.getLogger(__name__)


class WebTransportProtocol(QuicConnectionProtocol):
    """
    Protocol handler for WebTransport over HTTP/3.
    Handles connection setup, routing, and dispatching to appropriate handlers.
    """

    def __init__(
        self,
        *args,
        handler_map: Dict[bytes, Type[WebTransportHandler]] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._http: Optional[H3Connection] = None
        self._handler: Optional[WebTransportHandler] = None
        # Map path prefixes to handler classes
        self._handler_map = handler_map or {}

    def quic_event_received(self, event: QuicEvent) -> None:
        """Handle QUIC protocol events."""
        if isinstance(event, ProtocolNegotiated):
            self._http = H3Connection(self._quic, enable_webtransport=True)
            logger.debug("HTTP/3 connection established")
        elif isinstance(event, StreamReset) and self._handler is not None:
            # Handle stream resets (abnormal closure)
            self._handler.stream_closed(event.stream_id)
            logger.debug(f"Stream {event.stream_id} reset")

        if self._http is not None:
            for h3_event in self._http.handle_event(event):
                self._h3_event_received(h3_event)

    def _h3_event_received(self, event: H3Event) -> None:
        """Process HTTP/3 events."""
        if isinstance(event, HeadersReceived):
            self._process_headers(event)

        if self._handler:
            self._handler.h3_event_received(event)

    def _process_headers(self, event: HeadersReceived) -> None:
        """Process HTTP headers to establish WebTransport sessions."""
        headers = dict(event.headers)

        # Check if this is a WebTransport request
        if (
            headers.get(b":method") == b"CONNECT"
            and headers.get(b":protocol") == b"webtransport"
        ):
            self._handshake_webtransport(event.stream_id, headers)
        else:
            self._send_response(event.stream_id, 400, end_stream=True)
            logger.warning("Received non-WebTransport request")

    def _handshake_webtransport(
        self, stream_id: int, request_headers: Dict[bytes, bytes]
    ) -> None:
        """Handle WebTransport session establishment."""
        authority = request_headers.get(b":authority")
        path = request_headers.get(b":path")

        if authority is None or path is None:
            # Required headers missing
            self._send_response(stream_id, 400, end_stream=True)
            logger.warning("WebTransport handshake missing required headers")
            return

        # Find an appropriate handler for this path
        handler_cls = None
        for path_prefix, cls in self._handler_map.items():
            if path.startswith(path_prefix):
                handler_cls = cls
                break

        if handler_cls:
            if self._handler is not None:
                # Only one handler per connection for now
                logger.warning(
                    "Multiple WebTransport sessions on same connection not supported"
                )
                self._send_response(stream_id, 409, end_stream=True)  # Conflict
                return

            self._handler = handler_cls(stream_id, self._http)
            self._send_response(stream_id, 200)
            logger.info(
                f"WebTransport session established for path: {path.decode('ascii', errors='replace')}"
            )
        else:
            self._send_response(stream_id, 404, end_stream=True)
            logger.warning(
                f"No handler found for path: {path.decode('ascii', errors='replace')}"
            )

    def _send_response(
        self, stream_id: int, status_code: int, end_stream=False
    ) -> None:
        """Send an HTTP response."""
        headers = [(b":status", str(status_code).encode())]
        if status_code == 200:
            headers.append((b"sec-webtransport-http3-draft", b"draft02"))
        self._http.send_headers(
            stream_id=stream_id, headers=headers, end_stream=end_stream
        )
