"""
Session management for toxolib
"""
import os
import logging
import atexit
import base64
import time
import threading
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import keyring
import paramiko

import socket
import os
import tempfile
import json
import pickle
import signal
import atexit
import time

# Session data
_SESSION = {
    'credentials': {},
    'connections': {},
    'initialized': False,
    'keep_alive_thread': None
}

# Path to store connection information
_CONNECTION_FILE = os.path.expanduser("~/.toxolib/connections.json")
_CREDENTIAL_FILE = os.path.expanduser("~/.toxolib/credentials.bin")

# Ensure directory exists
os.makedirs(os.path.dirname(_CONNECTION_FILE), exist_ok=True)

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
    
    key = f"{hostname}:{username}"
    if password:
        encrypted_password = _encrypt_password(password)
        _SESSION['credentials'][key] = encrypted_password
        
        # Save credentials to file
        _save_credentials(_SESSION['credentials'])
        return True
    return False

def get_credentials(hostname, username):
    """Get credentials from the session"""
    if not _SESSION['initialized']:
        initialize_session()
    
    key = f"{hostname}:{username}"
    encrypted_password = _SESSION['credentials'].get(key)
    
    if encrypted_password:
        return _decrypt_password(encrypted_password)
    return None

def store_connection(hostname, username, ssh_client, sftp_client):
    """Store an SSH connection in the session"""
    if not _SESSION['initialized']:
        initialize_session()
    
    key = f"{username}@{hostname}"
    _SESSION['connections'][key] = {
        'ssh': ssh_client,
        'sftp': sftp_client,
        'last_used': time.time()
    }
    
    # Save connection info to file
    connections = _load_connections()
    connections[key] = {
        'hostname': hostname,
        'username': username,
        'last_used': time.time()
    }
    _save_connections(connections)
    
    # Start keep-alive thread if not already running
    _start_keep_alive_thread()
    
    return True

def get_connection(hostname, username):
    """Get an SSH connection from the session"""
    if not _SESSION['initialized']:
        initialize_session()
    
    key = f"{username}@{hostname}"
    connection = _SESSION['connections'].get(key)
    
    if connection:
        # Update last used timestamp
        connection['last_used'] = time.time()
        return connection['ssh'], connection['sftp']
    
    return None, None

def _keep_alive_connections():
    """Send keep-alive packets to all stored connections"""
    while _SESSION.get('connections'):
        current_time = time.time()
        connections_to_remove = []
        
        for key, connection in _SESSION['connections'].items():
            try:
                # Check if connection is still active
                if current_time - connection['last_used'] > 600:  # 10 minutes timeout
                    # Close connection if not used for 10 minutes
                    logging.info(f"Closing inactive connection: {key}")
                    connections_to_remove.append(key)
                    continue
                    
                # Send keep-alive packet
                transport = connection['ssh'].get_transport()
                if transport and transport.is_active():
                    transport.send_ignore()
                    logging.debug(f"Sent keep-alive packet to {key}")
                else:
                    # Connection is dead, remove it
                    logging.info(f"Connection lost: {key}")
                    connections_to_remove.append(key)
            except Exception as e:
                logging.error(f"Error in keep-alive for {key}: {e}")
                connections_to_remove.append(key)
        
        # Remove dead connections
        for key in connections_to_remove:
            close_connection(key)
            
        # Sleep for 30 seconds before next check
        time.sleep(30)
    
    # No more connections, thread can exit
    _SESSION['keep_alive_thread'] = None
    logging.debug("Keep-alive thread stopped")

def _start_keep_alive_thread():
    """Start the keep-alive thread if not already running"""
    if not _SESSION.get('keep_alive_thread') or not _SESSION['keep_alive_thread'].is_alive():
        _SESSION['keep_alive_thread'] = threading.Thread(
            target=_keep_alive_connections,
            daemon=True  # Make thread daemon so it exits when main thread exits
        )
        _SESSION['keep_alive_thread'].start()
        logging.debug("Keep-alive thread started")

def close_connection(connection_key):
    """Close a specific connection"""
    if connection_key in _SESSION['connections']:
        connection = _SESSION['connections'][connection_key]
        try:
            if connection['sftp']:
                connection['sftp'].close()
            if connection['ssh']:
                connection['ssh'].close()
        except Exception as e:
            logging.error(f"Error closing connection {connection_key}: {e}")
        finally:
            del _SESSION['connections'][connection_key]
            logging.info(f"Connection closed: {connection_key}")
            
            # Remove from connection file
            connections = _load_connections()
            if connection_key in connections:
                del connections[connection_key]
                _save_connections(connections)

def clear_connections():
    """Close all stored connections"""
    for key in list(_SESSION['connections'].keys()):
        close_connection(key)

def clear_credentials(hostname=None, username=None, force=False):
    """Clear stored credentials
    
    Args:
        hostname (str, optional): Hostname to clear credentials for. If None, clears all credentials.
        username (str, optional): Username to clear credentials for. If None, clears all credentials for the hostname.
        force (bool, optional): If True, force clear credentials even if persistence is enabled.
    """
    # Don't clear credentials unless forced
    if not force:
        return
        
    if hostname and username:
        # Clear specific credentials
        key = f"{hostname}:{username}"
        if key in _SESSION['credentials']:
            del _SESSION['credentials'][key]
            logging.info(f"Credentials cleared for {username}@{hostname}")
    elif hostname:
        # Clear all credentials for this hostname
        keys_to_remove = [k for k in _SESSION['credentials'].keys() if k.startswith(f"{hostname}:")]
        for key in keys_to_remove:
            del _SESSION['credentials'][key]
        if keys_to_remove:
            logging.info(f"All credentials cleared for {hostname}")
    else:
        # Clear all credentials
        _SESSION['credentials'] = {}
        logging.info("All session credentials cleared")

def _load_connections():
    """Load connection information from file"""
    if os.path.exists(_CONNECTION_FILE):
        try:
            with open(_CONNECTION_FILE, 'r') as f:
                connections = json.load(f)
                return connections
        except Exception as e:
            logging.error(f"Error loading connections: {e}")
    return {}

def _save_connections(connections):
    """Save connection information to file"""
    try:
        with open(_CONNECTION_FILE, 'w') as f:
            json.dump(connections, f)
    except Exception as e:
        logging.error(f"Error saving connections: {e}")

def _load_credentials():
    """Load encrypted credentials from file"""
    if os.path.exists(_CREDENTIAL_FILE):
        try:
            with open(_CREDENTIAL_FILE, 'rb') as f:
                encrypted_data = f.read()
                key = _get_encryption_key()
                f = Fernet(key)
                decrypted_data = f.decrypt(encrypted_data)
                return pickle.loads(decrypted_data)
        except Exception as e:
            logging.error(f"Error loading credentials: {e}")
    return {}

def _save_credentials(credentials):
    """Save encrypted credentials to file"""
    try:
        key = _get_encryption_key()
        f = Fernet(key)
        pickled_data = pickle.dumps(credentials)
        encrypted_data = f.encrypt(pickled_data)
        with open(_CREDENTIAL_FILE, 'wb') as f:
            f.write(encrypted_data)
    except Exception as e:
        logging.error(f"Error saving credentials: {e}")

def initialize_session():
    """Initialize the session"""
    if not _SESSION['initialized']:
        # Load existing connections and credentials
        _SESSION['credentials'] = _load_credentials()
        
        # Register cleanup on exit - but only for the process, not the connections
        atexit.register(lambda: _save_credentials(_SESSION['credentials']))
        
        _SESSION['initialized'] = True
        logging.debug("Session initialized")
        
        # Start the keep-alive thread
        _start_keep_alive_thread()
