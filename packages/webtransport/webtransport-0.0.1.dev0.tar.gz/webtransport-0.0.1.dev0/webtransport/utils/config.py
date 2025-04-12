"""
Configuration utilities for WebTransport server.
"""

import argparse
import logging
import os

# Default server configuration
DEFAULT_HOST = "::1"
DEFAULT_PORT = 4433
DEFAULT_CERTFILE = "certificate.pem"
DEFAULT_KEYFILE = "certificate.key"

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for the WebTransport server."""
    parser = argparse.ArgumentParser(description="WebTransport over HTTP/3 server")
    parser.add_argument(
        "--host",
        type=str,
        default=DEFAULT_HOST,
        help=f"Host to bind to (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to bind to (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--certificate",
        type=str,
        default=DEFAULT_CERTFILE,
        help=f"TLS certificate file (default: {DEFAULT_CERTFILE})",
    )
    parser.add_argument(
        "--key",
        type=str,
        default=DEFAULT_KEYFILE,
        help=f"TLS private key file (default: {DEFAULT_KEYFILE})",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    return parser.parse_args()


def check_certificate_files(cert_path: str, key_path: str) -> bool:
    """
    Check if certificate files exist.

    Args:
        cert_path: Path to the certificate file
        key_path: Path to the key file

    Returns:
        True if both files exist, False otherwise
    """
    for file_path in [cert_path, key_path]:
        if not os.path.isfile(file_path):
            logger.error(f"Cannot find {file_path}. Please check the path.")
            return False
    return True
