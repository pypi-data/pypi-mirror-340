#!/usr/bin/env python3

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
An example WebTransport over HTTP/3 server based on the aioquic library.
Processes incoming streams and datagrams, and
replies with the ASCII-encoded length of the data sent in bytes.
Example use:
  python3 webtransport_server.py certificate.pem certificate.key
Example use from JavaScript:
  let transport = new WebTransport("https://localhost:4433/counter");
  await transport.ready;
  let stream = await transport.createBidirectionalStream();
  let encoder = new TextEncoder();
  let writer = stream.writable.getWriter();
  await writer.write(encoder.encode("Hello, world!"))
  writer.close();
  console.log(await new Response(stream.readable).text());
This will output "13" (the length of "Hello, world!") into the console.
"""

# ---- Dependencies ----
#
# This server only depends on Python standard library and aioquic 0.9.19 or
# later. See https://github.com/aiortc/aioquic for instructions on how to
# install aioquic.
#
# ---- Certificates ----
#
# HTTP/3 always operates using TLS, meaning that running a WebTransport over
# HTTP/3 server requires a valid TLS certificate.  The easiest way to do this
# is to get a certificate from a real publicly trusted CA like
# <https://letsencrypt.org/>.
# https://developers.google.com/web/fundamentals/security/encrypt-in-transit/enable-https
# contains a detailed explanation of how to achieve that.
#
# As an alternative, Chromium can be instructed to trust a self-signed
# certificate using command-line flags.  Here are step-by-step instructions on
# how to do that:
#
#   1. Generate a certificate and a private key:
#         openssl req -newkey rsa:2048 -nodes -keyout certificate.key \
#                   -x509 -out certificate.pem -subj '/CN=Test Certificate' \
#                   -addext "subjectAltName = DNS:localhost"
#
#   2. Compute the fingerprint of the certificate:
#         openssl x509 -pubkey -noout -in certificate.pem |
#                   openssl rsa -pubin -outform der |
#                   openssl dgst -sha256 -binary | base64
#      The result should be a base64-encoded blob that looks like this:
#          "Gi/HIwdiMcPZo2KBjnstF5kQdLI5bPrYJ8i3Vi6Ybck="
#
#   3. Pass a flag to Chromium indicating what host and port should be allowed
#      to use the self-signed certificate.  For instance, if the host is
#      localhost, and the port is 4433, the flag would be:
#         --origin-to-force-quic-on=localhost:4433
#
#   4. Pass a flag to Chromium indicating which certificate needs to be trusted.
#      For the example above, that flag would be:
#         --ignore-certificate-errors-spki-list=Gi/HIwdiMcPZo2KBjnstF5kQdLI5bPrYJ8i3Vi6Ybck=
#
# See https://www.chromium.org/developers/how-tos/run-chromium-with-flags for
# details on how to run Chromium with flags.

"""
Core WebTransport server implementation.
"""

import asyncio
import logging
from typing import Dict, List, Type

from aioquic.asyncio import serve
from aioquic.h3.connection import H3_ALPN
from aioquic.quic.configuration import QuicConfiguration

from .handlers.base import WebTransportHandler
from .handlers.counter import CounterHandler
from .protocols.http3 import WebTransportProtocol

logger = logging.getLogger(__name__)


async def start_server(
    host: str,
    port: int,
    certificate: str,
    private_key: str,
    handler_map: Dict[bytes, Type[WebTransportHandler]] = None,
    alpn_protocols: List[str] = H3_ALPN,
    max_datagram_size: int = 65536,
) -> asyncio.AbstractServer:
    """
    Start a WebTransport server with the specified configuration.

    Args:
        host: Host to bind to
        port: Port to bind to
        certificate: Path to the TLS certificate file
        private_key: Path to the TLS private key file
        handler_map: Mapping of URL paths to handler classes
        alpn_protocols: ALPN protocols to advertise
        max_datagram_size: Maximum datagram frame size

    Returns:
        The server object
    """
    configuration = QuicConfiguration(
        alpn_protocols=alpn_protocols,
        is_client=False,
        max_datagram_frame_size=max_datagram_size,
    )

    try:
        configuration.load_cert_chain(certificate, private_key)
    except Exception as e:
        logger.error(f"Failed to load certificate: {e}")
        raise

    # Default handler map if none provided
    if handler_map is None:
        handler_map = {b"/counter": CounterHandler}

    def create_protocol(*args, **kwargs):
        return WebTransportProtocol(*args, handler_map=handler_map, **kwargs)

    return await serve(
        host,
        port,
        configuration=configuration,
        create_protocol=create_protocol,
    )
