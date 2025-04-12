#!/usr/bin/env python3
"""
Main entry point for the WebTransport server when run as a command-line application.
"""

import asyncio
import logging
import sys
from typing import Dict, Type

# Import from the package structure following the refactoring plan
from .handlers.base import WebTransportHandler
from .handlers.counter import CounterHandler
from .handlers.echo import EchoHandler
from .server import start_server
from .utils.config import check_certificate_files, parse_args
from .utils.logging import configure_logging

logger = logging.getLogger(__name__)


def main() -> int:
    """
    Main entry point when running as a script.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    # Parse command line arguments
    args = parse_args()

    # Configure logging
    configure_logging(level=logging.DEBUG if args.verbose else logging.INFO)

    # Check certificate files
    if not check_certificate_files(args.certificate, args.key):
        return 1

    # Default handler map - paths to handler classes
    handler_map: Dict[bytes, Type[WebTransportHandler]] = {
        b"/counter": CounterHandler,
        b"/echo": EchoHandler,
    }

    # Start server
    loop = asyncio.get_event_loop()
    try:
        server = loop.run_until_complete(
            start_server(
                host=args.host,
                port=args.port,
                certificate=args.certificate,
                private_key=args.key,
                handler_map=handler_map,
            )
        )

        logger.info(f"WebTransport server running on https://{args.host}:{args.port}")
        logger.info(f"Available handlers: {', '.join(p.decode() for p in handler_map.keys())}")

        loop.run_forever()
        return 0
    except KeyboardInterrupt:
        logger.info("Server shutting down")
        return 0
    except Exception as e:
        logger.error(f"Server error: {e}")
        return 1
    finally:
        loop.close()


if __name__ == "__main__":
    sys.exit(main())
