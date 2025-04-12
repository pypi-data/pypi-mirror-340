"""
Certificate utilities for WebTransport server.
"""

import base64
import logging
import os
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)

def generate_self_signed_cert(
    host: str = "localhost",
    cert_path: str = "certificate.pem",
    key_path: str = "certificate.key"
) -> bool:
    """
    Generate a self-signed certificate for testing.

    Args:
        host: Hostname to use in the certificate
        cert_path: Path to write the certificate
        key_path: Path to write the private key

    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = [
            "openssl", "req", "-newkey", "rsa:2048", "-nodes",
            "-keyout", key_path, "-x509", "-out", cert_path,
            "-subj", f"/CN=Test Certificate", "-addext", f"subjectAltName = DNS:{host}"
        ]

        subprocess.run(cmd, check=True, capture_output=True)

        # Set permissions
        os.chmod(key_path, 0o600)
        os.chmod(cert_path, 0o644)

        logger.info(f"Generated certificate at {cert_path} and key at {key_path}")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to generate certificate: {e.stderr.decode()}")
        return False
    except Exception as e:
        logger.error(f"Failed to generate certificate: {e}")
        return False

def get_certificate_fingerprint(cert_path: str) -> Optional[str]:
    """
    Get the SHA-256 fingerprint of a certificate.

    Args:
        cert_path: Path to the certificate file

    Returns:
        Base64-encoded fingerprint, or None if failed
    """
    try:
        # Extract the public key
        cmd1 = ["openssl", "x509", "-pubkey", "-noout", "-in", cert_path]
        pubkey = subprocess.run(cmd1, check=True, capture_output=True).stdout

        # Convert to DER format
        cmd2 = ["openssl", "rsa", "-pubin", "-outform", "der"]
        der = subprocess.run(cmd2, input=pubkey, check=True, capture_output=True).stdout

        # Calculate SHA-256 digest
        cmd3 = ["openssl", "dgst", "-sha256", "-binary"]
        digest = subprocess.run(cmd3, input=der, check=True, capture_output=True).stdout

        # Encode in base64
        fingerprint = base64.b64encode(digest).decode('ascii')

        logger.info(f"Certificate fingerprint: {fingerprint}")
        return fingerprint

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get certificate fingerprint: {e.stderr.decode()}")
        return None
    except Exception as e:
        logger.error(f"Failed to get certificate fingerprint: {e}")
        return None
