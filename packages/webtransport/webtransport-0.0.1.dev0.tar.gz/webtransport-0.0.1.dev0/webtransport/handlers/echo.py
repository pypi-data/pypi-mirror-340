"""
Echo handler for WebTransport connections.
"""

import logging

from aioquic.h3.events import (DatagramReceived, H3Event,
                               WebTransportStreamDataReceived)
from aioquic.quic.connection import stream_is_unidirectional

from .base import WebTransportHandler

logger = logging.getLogger(__name__)

class EchoHandler(WebTransportHandler):
    """
    Echo handler that sends back exactly what it receives.
    """

    def h3_event_received(self, event: H3Event) -> None:
        if isinstance(event, DatagramReceived):
            # Echo the datagram back
            self._http.send_datagram(self._session_id, event.data)
            logger.debug(f"Echo datagram of length {len(event.data)}")

        elif isinstance(event, WebTransportStreamDataReceived):
            if event.stream_ended:
                if stream_is_unidirectional(event.stream_id):
                    # For unidirectional streams, create a new stream for the response
                    response_id = self._http.create_webtransport_stream(
                        self._session_id, is_unidirectional=True)
                else:
                    # For bidirectional streams, use the same stream
                    response_id = event.stream_id

                # Echo the data back
                self._http._quic.send_stream_data(
                    response_id, event.data, end_stream=True)
                logger.debug(f"Echo stream {event.stream_id}, response on {response_id}")
