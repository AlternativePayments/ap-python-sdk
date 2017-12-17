# Alternative Payments Python bindings
# API docs at http://www.alternativepayments.com/support/api/index.html
# Authors:
# Marjan Stojanovic <marjan.stojanovic90@gmail.com>
# Marjan Stojanovic <nenad.bozic@smartcat.io>

# Configuration variables

api_secret_key = None
api_public_key = None
api_base = 'https://api.alternativepayments.com/api'
api_version = None
default_http_client = None

# Resource

from ap_python_sdk.util import json, logger
from ap_python_sdk.version import VERSION
