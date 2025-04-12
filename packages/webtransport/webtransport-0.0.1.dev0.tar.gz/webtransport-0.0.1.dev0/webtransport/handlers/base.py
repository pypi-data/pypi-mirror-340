"""
Base handler class for WebTransport connections.
"""

import logging

from aioquic.h3.connection import H3Connection
from aioquic.h3.events import H3Event

logger = logging.getLogger(__name__)


class WebTransportHandler:
    """Base handler class for WebTransport connections."""

    def __init__(self, session_id: int, http: H3Connection) -> None:
        """
        Initialize the handler with a session ID and HTTP connection.

        Args:
            session_id: The WebTransport session ID
            http: The HTTP/3 connection
        """
        self._session_id = session_id
        self._http = http

    def h3_event_received(self, event: H3Event) -> None:
        """
        Process HTTP/3 events.

        Args:
            event: The HTTP/3 event to process
        """
        pass

    def stream_closed(self, stream_id: int) -> None:
        """
        Handle stream closure.

        Args:
            stream_id: The ID of the closed stream
        """
        pass
