import base64
import logging
import os
import sys


logger = logging.getLogger('alternative_payments')

__all__ = ['StringIO', 'parse_qsl', 'json', 'utf8']

try:
    # When cStringIO is available
    import cStringIO as StringIO
except ImportError:
    import StringIO

try:
    from urlparse import parse_qsl
except ImportError:
    # Python < 2.6
    from cgi import parse_qsl

try:
    import json
except ImportError:
    json = None

if not (json and hasattr(json, 'loads')):
    try:
        import simplejson as json
    except ImportError:
        if not json:
            raise ImportError(
                "Alternative Payments requires a JSON library, such as simplejson. "
                "HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' or "
                "'easy_install simplejson'.")
        else:
            raise ImportError(
                "Alternative Payments requires a JSON library with the same interface as "
                "the Python 2.6 'json' library.  You appear to have a 'json' "
                "library with a different interface.  Please install "
                "the simplejson library.  HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' "
                "or 'easy_install simplejson'.")


def utf8(value):
    if isinstance(value, unicode) and sys.version_info < (3, 0):
        return value.encode('utf-8')
    else:
        return value

def encode_key(key):
    if sys.version_info < (3, 0):
        return base64.b64encode(key)
    else:
        return base64.b64encode(key.encode('utf-8')).decode()
