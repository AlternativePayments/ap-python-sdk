from ap_python_sdk import error, http_client, version, util
import ap_python_sdk
import calendar
import datetime
import time
import urllib
import urlparse


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _encode_nested_dict(key, data, fmt='%s[%s]'):
    d = {}
    for subkey, subvalue in data.iteritems():
        d[fmt % (key, subkey)] = subvalue
    return d


def _api_encode(data):
    for key, value in data.iteritems():
        key = util.utf8(key)
        if value is None:
            continue
        elif isinstance(value, list) or isinstance(value, tuple):
            for sv in value:
                if isinstance(sv, dict):
                    subdict = _encode_nested_dict(key, sv, fmt='%s[][%s]')
                    for k, v in _api_encode(subdict):
                        yield (k, v)
                else:
                    yield ("%s[]" % (key,), util.utf8(sv))
        elif isinstance(value, dict):
            subdict = _encode_nested_dict(key, value)
            for subkey, subvalue in _api_encode(subdict):
                yield (subkey, subvalue)
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, util.utf8(value))


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urlparse.urlsplit(url)

    if base_query:
        query = '%s&%s' % (base_query, query)

    return urlparse.urlunsplit((scheme, netloc, path, query, fragment))


class APIRequester(object):

    def __init__(self, key=None, public_key=None, client=None, api_base=None, account=None):
        self.api_base = api_base or ap_python_sdk.api_base
        self.api_secret_key = key
        self.api_public_key = public_key

        self._client = client or ap_python_sdk.default_http_client or \
            http_client.new_default_http_client()

    @classmethod
    def api_url(cls, url=''):
        return '%s%s' % (ap_python_sdk.api_base, url)

    @classmethod
    def encode(cls, d):
        return urllib.urlencode(list(_api_encode(d)))

    @classmethod
    def build_url(cls, url, params):
        return _build_api_url(url, cls.encode(params))

    def request(self, method, url, params=None, headers=None):
        rbody, rcode = self.request_raw(
            method.lower(), url, params, headers)
        resp = self.interpret_response(rbody, rcode)
        return resp

    def handle_api_error(self, rbody, rcode, error_response):
        try:
            error_type = error_response['Type']
            if error_type == 'payment_error':
                raise error.PaymentError(error_response['Message'], rcode, error_response['Code'])
            elif error_type == 'api_error':
                raise error.APIError(error_response['Message'], rcode, error_response['Code'])
            elif error_type == 'invalid_parameter_error':
                raise error.InvalidParameterError(error_response['Message'], rcode, error_response['Code'], error_response['Param'])
            else:
                raise error.APIError(error_response['Message'], rcode, error_response['Code']);
        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (rbody, rcode),
                rbody, rcode, error_response)

    def request_raw(self, method, url, params=None, supplied_headers=None):
        if self.api_secret_key:
            my_api_secret_key = self.api_secret_key
        else:
            from ap_python_sdk import api_secret_key
            my_api_secret_key = api_secret_key

        if self.api_public_key:
            my_api_public_key = self.api_public_key
        else:
            from ap_python_sdk import api_public_key
            my_api_public_key = api_public_key

        if my_api_secret_key is None:
            raise error.AuthenticationError(
                'No secret API key provided. (HINT: set your secret API key using '
                '"ap_python_sdk.api_secret_key = <API-KEY>").')

        if my_api_public_key is None:
            raise error.AuthenticationError(
                'No public API key provided. (HINT: set your public API key using '
                '"ap_python_sdk.api_public_key = <API-KEY>").')

        abs_url = '%s%s' % (self.api_base, url)

        encoded_params = urllib.urlencode(list(_api_encode(params or {})))

        if method == 'get' or method == 'delete':
            if params:
                abs_url = _build_api_url(abs_url, encoded_params)
            post_data = None
        elif method == 'post':
                post_data = util.json.dumps(params or {})
        else:
            raise error.APIError(
                'Unrecognized HTTP method %r.' % (method))

        headers = {
            'User-Agent': 'AlternativePayments Python SDK v%s' % (version.VERSION),
            'Authorization': 'Basic %s' % (util.encode_key(my_api_secret_key),),
            'Content-Type': 'application/json'
        }


        if supplied_headers is not None:
            for key, value in supplied_headers.items():
                headers[key] = value

        rbody, rcode = self._client.request(
            method, abs_url, headers, post_data)

        util.logger.info('%s %s %d', method.upper(), abs_url, rcode)
        util.logger.debug(
            'API request to %s returned (response code, response body) of '
            '(%d, %r)',
            abs_url, rcode, rbody)
        return rbody, rcode

    def interpret_response(self, rbody, rcode):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
            resp = util.json.loads(rbody)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody, rcode)
        if not (200 <= rcode < 300):
            self.handle_api_error(rbody, rcode, resp)
        return resp
