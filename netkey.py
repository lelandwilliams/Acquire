""" Shared-key check for websocket connections.

A Concierge generates a random key and passes it to every process it
starts (game servers, GM, robots) in the ACQUIRE_KEY environment variable.
Clients put the key in the query string of the URL they connect to, and
the concierge and game servers drop connections without the right key.
This keeps processes from one game from joining another game running
on the same machine.
"""
import os
from PyQt5.QtCore import QUrlQuery

KEY_ENV = 'ACQUIRE_KEY'

def env_key():
    """ The key passed down by the concierge, or '' if there is none """
    return os.environ.get(KEY_ENV, '')

def add_key(url, key):
    """ Adds key to the query string of a QUrl """
    if key:
        query = QUrlQuery()
        query.addQueryItem('key', key)
        url.setQuery(query)

def has_key(socket, key):
    """ True if a connected QWebSocket opened its URL with key """
    return QUrlQuery(socket.requestUrl()).queryItemValue('key') == key
