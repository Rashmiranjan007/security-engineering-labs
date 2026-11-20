"""Educational cryptography CLI: AES-GCM and HMAC-SHA-256.

Production keys must be held by a KMS/HSM or secrets manager, not this process.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import sys
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY_ENV = "LAB_AES_KEY_B64"
NONCE_BYTES = 12
KEY_BYTES = 32


class CryptoInputError(ValueError):
    """Raised for invalid or unsafe lab input."""


def load_aes_key(value: str | None = None) -> bytes:
    """Load a 32-byte AES key from strict base64 input."""
    encoded = value if value is not None else os.environ.get(KEY_ENV, "")
    if not encoded:
        raise CryptoInputError(f"Set {KEY_ENV} to a base64-encoded 32-byte demo key.")
    try:
        key = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise CryptoInputError("Key must be valid base64.") from exc
    if len(key) != KEY_BYTES:
        raise CryptoInputError("AES-256-GCM requires exactly 32 key bytes.")
    return key


def encrypt(plaintext: bytes, key: bytes, aad: bytes = b"") -> dict[str, str | int]:
    """Encrypt bytes with AES-256-GCM and return a JSON-safe envelope."""
    if len(key) != KEY_BYTES:
        raise CryptoInputError("AES-256-GCM requires exactly 32 key bytes.")
    nonce = secrets.token_bytes(NONCE_BYTES)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    return {
        "version": 1,
        "algorithm": "AES-256-GCM",
        "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
        "aad_b64": base64.b64encode(aad).decode("ascii"),
    }


def decrypt(envelope: dict[str, Any], key: bytes, aad: bytes | None = None) -> bytes:
    """Authenticate and decrypt an envelope; fail closed on tampering."""
    if len(key) != KEY_BYTES:
        raise CryptoInputError("AES-256-GCM requires exactly 32 key bytes.")
    if envelope.get("version") != 1 or envelope.get("algorithm") != "AES-256-GCM":
        raise CryptoInputError("Unsupported envelope version or algorithm.")
    try:
        nonce = base64.b64decode(envelope["nonce_b64"], validate=True)
        ciphertext = base64.b64decode(envelope["ciphertext_b64"], validate=True)
        stored_aad = base64.b64decode(envelope["aad_b64"], validate=True)
    except (KeyError, ValueError, TypeError) as exc:
        raise CryptoInputError("Malformed envelope.") from exc
    if len(nonce) != NONCE_BYTES:
        raise CryptoInputError("AES-GCM nonce must be exactly 12 bytes.")
    selected_aad = stored_aad if aad is None else aad
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, selected_aad)
    except InvalidTag as exc:
        raise CryptoInputError("Authentication failed: wrong key, AAD, or modified envelope.") from exc


def create_hmac(message: bytes, key: bytes) -> str:
    """Return a hex-encoded HMAC-SHA-256 tag."""
    if len(key) < 32:
        raise CryptoInputError("Use at least 32 bytes of key material for this lab.")
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def verify_hmac(message: bytes, key: bytes, tag_hex: str) -> bool:
    """Verify a HMAC tag using constant-time comparison."""
    try:
        supplied = bytes.fromhex(tag_hex)
    except ValueError:
        return False
    expected = hmac.new(key, message, hashlib.sha256).digest()
    return len(key) >= 32 and hmac.compare_digest(expected, supplied)


def _read_envelope(path: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CryptoInputError(f"Cannot read envelope: {exc}") from exc
    if not isinstance(data, dict):
        raise CryptoInputError("Envelope must be a JSON object.")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Local AES-256-GCM demo")
    sub = parser.add_subparsers(dest="command", required=True)
    enc = sub.add_parser("encrypt")
    enc.add_argument("--text", required=True)
    enc.add_argument("--aad", default="")
    enc.add_argument("--out")
    dec = sub.add_parser("decrypt")
    dec.add_argument("--input", required=True)
    dec.add_argument("--aad")
    args = parser.parse_args()
    try:
        key = load_aes_key()
        if args.command == "encrypt":
            result = encrypt(args.text.encode("utf-8"), key, args.aad.encode("utf-8"))
            rendered = json.dumps(result, indent=2)
            if args.out:
                Path(args.out).write_text(rendered + "\n", encoding="utf-8")
                print(f"Encrypted envelope written to {args.out}")
            else:
                print(rendered)
        else:
            aad = None if args.aad is None else args.aad.encode("utf-8")
            plaintext = decrypt(_read_envelope(args.input), key, aad)
            print(plaintext.decode("utf-8"))
        return 0
    except (CryptoInputError, UnicodeDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
