"""
Counter handler for WebTransport connections.
"""

import logging
from collections import defaultdict

from aioquic.h3.connection import H3Connection
from aioquic.h3.events import (DatagramReceived, H3Event,
                               WebTransportStreamDataReceived)
from aioquic.quic.connection import stream_is_unidirectional

from .base import WebTransportHandler

logger = logging.getLogger(__name__)

class CounterHandler(WebTransportHandler):
    """
    A sample WebTransport handler that counts bytes and echoes lengths.

    - For every incoming bidirectional stream, counts bytes received until closed,
      then replies with the count on the same stream.
    - For every incoming unidirectional stream, counts bytes received until closed,
      then replies with the count on a new unidirectional stream.
    - For every incoming datagram, sends a datagram with the length of datagram received.
    """

    def __init__(self, session_id: int, http: H3Connection) -> None:
        super().__init__(session_id, http)
        self._counters = defaultdict(int)

    def h3_event_received(self, event: H3Event) -> None:
        if isinstance(event, DatagramReceived):
            self._handle_datagram(event)
        elif isinstance(event, WebTransportStreamDataReceived):
            self._handle_stream_data(event)

    def _handle_datagram(self, event: DatagramReceived) -> None:
        """Process received datagrams by echoing their length."""
        payload = str(len(event.data)).encode('ascii')
        self._http.send_datagram(self._session_id, payload)
        logger.debug(f"Datagram of length {len(event.data)} received and processed")

    def _handle_stream_data(self, event: WebTransportStreamDataReceived) -> None:
        """Process data received on a stream."""
        self._counters[event.stream_id] += len(event.data)

        if event.stream_ended:
            if stream_is_unidirectional(event.stream_id):
                response_id = self._http.create_webtransport_stream(
                    self._session_id, is_unidirectional=True)
            else:
                response_id = event.stream_id

            payload = str(self._counters[event.stream_id]).encode('ascii')
            self._http._quic.send_stream_data(response_id, payload, end_stream=True)
            self.stream_closed(event.stream_id)
            logger.debug(f"Stream {event.stream_id} ended, sent response on {response_id}")

    def stream_closed(self, stream_id: int) -> None:
        """Clean up resources for closed streams."""
        try:
            del self._counters[stream_id]
            logger.debug(f"Stream {stream_id} closed and cleaned up")
        except KeyError:
            pass
