"""
A WebTransport over HTTP/3 server based on the aioquic library.
"""

import logging


logger = logging.getLogger(__name__)

# Default server configuration
DEFAULT_HOST = "::1"
DEFAULT_PORT = 4433
DEFAULT_CERTFILE = "certificate.pem"
DEFAULT_KEYFILE = "certificate.key"
