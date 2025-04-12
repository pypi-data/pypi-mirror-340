"""
Transport module for sending logs to Tropir API.
"""

import os
import requests
import threading
from .config import get_config


def send_log(log_data):
    """
    Sends log data to the Tropir API in a non-blocking way.
    
    Args:
        log_data (dict): The log data to send
    """
    config = get_config()
    if not config["enabled"]:
        return
    
    # Use a thread to handle the API call so it doesn't block
    def _send_request():
        try:
            requests.post(
                config["api_url"],
                json=log_data,
                timeout=3
            )
        except Exception as e:
            print(f"[TROPIR ERROR] Failed to send log: {e}")
    
    # Start a thread to handle the request
    thread = threading.Thread(target=_send_request)
    thread.daemon = True
    thread.start() 