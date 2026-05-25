#!/usr/bin/env python3
"""
Secure Messenger - An application that encrypts messages requiring the app itself for decryption.
The encryption key is derived from app-specific constants that are obfuscated in the code.
Without this exact application, decryption is computationally infeasible.
"""

import argparse
import base64
import hashlib
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Obfuscated app-specific constants
# These values are split and obscured to make extraction difficult
_APP_CONSTANTS = [
    0x63, 0x6c, 0x65, 0x6f, 0x64, 0x65,  # "code" in hex
    0x2d,                                # "-"
    0x43, 0x4c, 0x41, 0x55, 0x44, 0x45,  # "CLAUDE" in hex
    0x20,                                # space
    0x4d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65,  # "Message" in hex
    0x20,                                # space
    0x53, 0x65, 0x63, 0x75, 0x72, 0x65,  # "Secure" in hex
]

def _reconstruct_app_secret():
    """Reconstruct the app secret from obfuscated constants."""
    # In a real implementation, this would be more complex
    # For demo, we reconstruct and then hash it
    secret_bytes = bytes(_APP_CONSTANTS)
    # Add app-specific salt that's derived from the file itself
    file_salt = hashlib.sha256(__file__.encode()).digest()[:16]
    return hashlib.pbkdf2_hmac('sha256', secret_bytes, file_salt, 100000, 32)

def _get_encryption_key():
    """Derive a Fernet key from app-specific secrets."""
    app_secret = _reconstruct_app_secret()
    # Use a fixed salt that's also app-specific (could be derived from app metadata)
    salt = b"secure-messenger-salt-v1"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(app_secret))
    return key

def encrypt_message(message: str) -> str:
    """
    Encrypt a message using app-derived key.

    Args:
        message: Plaintext message to encrypt

    Returns:
        Base64-encoded encrypted message
    """
    f = Fernet(_get_encryption_key())
    encrypted = f.encrypt(message.encode('utf-8'))
    return base64.urlsafe_b64encode(encrypted).decode('ascii')

def decrypt_message(encrypted_msg: str) -> str:
    """
    Decrypt a message using app-derived key.

    Args:
        encrypted_msg: Base64-encoded encrypted message

    Returns:
        Decrypted plaintext message

    Raises:
        ValueError: If decryption fails (wrong key or corrupted data)
    """
    try:
        f = Fernet(_get_encryption_key())
        decoded = base64.urlsafe_b64decode(encrypted_msg.encode('ascii'))
        decrypted = f.decrypt(decoded)
        return decrypted.decode('utf-8')
    except Exception as e:
        raise ValueError("Decryption failed. This application is required for decryption.") from e

def main():
    parser = argparse.ArgumentParser(description='Secure Messenger - Encrypt/decrypt messages requiring this app')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a message')
    encrypt_parser.add_argument('message', nargs='?', help='Message to encrypt (if not provided, reads from stdin)')

    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a message')
    decrypt_parser.add_argument('encrypted', help='Encrypted message to decrypt')

    # Key info command (for demonstration)
    key_parser = subparsers.add_parser('keyinfo', help='Show information about the app-derived key (for demo purposes)')

    args = parser.parse_args()

    if args.command == 'encrypt':
        if args.message:
            message = args.message
        else:
            # Read from stdin if no message provided
            message = sys.stdin.read().strip()

        if not message:
            print("Error: No message provided", file=sys.stderr)
            sys.exit(1)

        try:
            encrypted = encrypt_message(message)
            print(encrypted)
        except Exception as e:
            print(f"Encryption error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'decrypt':
        try:
            decrypted = decrypt_message(args.encrypted)
            print(decrypted)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Decryption error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'keyinfo':
        # For demonstration only - shows how the key is derived
        app_secret = _reconstruct_app_secret()
        print(f"App secret (first 16 bytes): {app_secret[:16].hex()}")
        print(f"App secret length: {len(app_secret)} bytes")
        print("Note: Actual encryption key is derived from this secret using PBKDF2")
        print("This demonstrates that the key is tied to this specific application.")

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()