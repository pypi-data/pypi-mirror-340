"""
Session management for toxolib
"""
import os
import logging
import atexit
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import keyring

# Session data
_SESSION = {
    'credentials': {},
    'initialized': False
}

def _get_encryption_key():
    """Get encryption key from keyring or generate a new one"""
    # Use machine-specific salt
    salt = f"toxolib-{os.getlogin()}".encode()
    
    # Try to get key from keyring
    stored_key = keyring.get_password("toxolib", "session_key")
    
    if not stored_key:
        # Generate a new key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))
        # Store in keyring
        keyring.set_password("toxolib", "session_key", key.decode())
        return key
    
    return stored_key.encode()

def _encrypt_password(password):
    """Encrypt password for session storage"""
    if not password:
        return None
        
    key = _get_encryption_key()
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def _decrypt_password(encrypted_password):
    """Decrypt password from session storage"""
    if not encrypted_password:
        return None
        
    key = _get_encryption_key()
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

def store_credentials(hostname, username, password):
    """Store credentials for the session"""
    if not _SESSION['initialized']:
        initialize_session()
    
    key = f"{username}@{hostname}"
    if password:
        encrypted_password = _encrypt_password(password)
        _SESSION['credentials'][key] = encrypted_password
        return True
    return False

def get_credentials(hostname, username):
    """Get credentials from the session"""
    if not _SESSION['initialized']:
        initialize_session()
    
    key = f"{username}@{hostname}"
    encrypted_password = _SESSION['credentials'].get(key)
    
    if encrypted_password:
        return _decrypt_password(encrypted_password)
    return None

def clear_credentials():
    """Clear all stored credentials"""
    _SESSION['credentials'] = {}
    logging.info("Session credentials cleared")

def initialize_session():
    """Initialize the session"""
    if not _SESSION['initialized']:
        # Register cleanup on exit
        atexit.register(clear_credentials)
        _SESSION['initialized'] = True
        logging.debug("Session initialized")
