import sys
import urllib
import warnings

from ap_python_sdk import api_requester, error, util


def convert_to_ap_object(resp, api_key):
    types = {
        '/customer': Customer
    }

    if isinstance(resp, list):
        return [convert_to_ap_object(i, api_key) for i in resp]
    elif isinstance(resp, dict) and not isinstance(resp, BaseModel):
        resp = resp.copy()
        klass = types.get(api_key, BaseModel)
        return klass.construct_from(resp, api_key)
    else:
        return resp

def _compute_diff(current, previous):
    if isinstance(current, dict):
        previous = previous or {}
        diff = current.copy()
        for key in set(previous.keys()) - set(diff.keys()):
            diff[key] = ""
        return diff
    return current if current is not None else ""

def _serialize_list(array, previous):
    array = array or []
    previous = previous or []
    params = {}

    for i, v in enumerate(array):
        previous_item = previous[i] if len(previous) > i else None
        if hasattr(v, 'serialize'):
            params[str(i)] = v.serialize(previous_item)
        else:
            params[str(i)] = _compute_diff(v, previous_item)

    return params


class BaseModel(dict):
    def __init__(self, id=None, api_key=None, **params):
        super(BaseModel, self).__init__()

        self._unsaved_values = set()
        self._transient_values = set()

        self._retrieve_params = params
        self._previous = None

        object.__setattr__(self, 'api_key', api_key)

        if id:
            self['id'] = id

    def update(self, update_dict):
        for k in update_dict:
            self._unsaved_values.add(k)

        return super(BaseModel, self).update(update_dict)

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(BaseModel, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        if k[0] == '_' or k in self.__dict__:
            return super(BaseModel, self).__delattr__(k)
        else:
            del self[k]

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        super(BaseModel, self).__setitem__(k, v)

        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

        self._unsaved_values.add(k)

    def __getitem__(self, k):
        try:
            return super(BaseModel, self).__getitem__(k)
        except KeyError as err:
            raise err

    def __delitem__(self, k):
        super(BaseModel, self).__delitem__(k)

        # Allows for unpickling in Python 3.x
        if hasattr(self, '_unsaved_values'):
            self._unsaved_values.remove(k)

    @classmethod
    def construct_from(cls, values, key):
        instance = cls(values.get('id'), api_key=key)
        return instance

    @classmethod
    def api_base(cls):
        return None

    def request(self, method, url, params=None, headers=None):
        if params is None:
            params = self._retrieve_params
        requester = api_requester.APIRequester(
            key=self.api_key, api_base=self.api_base())
        response, api_key = requester.request(method, url, params, headers)

        return convert_to_ap_object(response, api_key)

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('id'), basestring):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return util.json.dumps(self, sort_keys=True, indent=2)

    def to_dict(self):
        return dict(self)

    def serialize(self, previous):
        params = {}
        unsaved_keys = self._unsaved_values or set()
        previous = previous or self._previous or {}

        for k, v in self.items():
            if k == 'id' or (isinstance(k, str) and k.startswith('_')):
                continue
            elif isinstance(v, APIResource):
                continue
            elif hasattr(v, 'serialize'):
                params[k] = v.serialize(previous.get(k, None))
            elif k in unsaved_keys:
                params[k] = _compute_diff(v, previous.get(k, None))
            elif k == 'additional_owners' and v is not None:
                params[k] = _serialize_list(v, previous.get(k, None))

        return params


class APIResource(BaseModel):

    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        instance = cls(id, api_key, **params)
        return instance

    @classmethod
    def class_name(cls):
        if cls == APIResource:
            raise NotImplementedError(
                'APIResource is an abstract class.  You should perform '
                'actions on its subclasses (e.g. Customer)')
        return str(urllib.quote_plus(cls.__name__.lower()))

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "/v1/%ss" % (cls_name,)

class ListObject(BaseModel):

    def list(self, **params):
        return self.request('get', self['url'], params)

    def all(self, **params):
        return self.list(**params)

    def auto_paging_iter(self):
        page = self
        params = dict(self._retrieve_params)

        while True:
            item_id = None
            for item in page:
                item_id = item.get('id', None)
                yield item

            if not getattr(page, 'has_more', False) or item_id is None:
                return

            params['starting_after'] = item_id
            page = self.list(**params)

    def create(self, idempotency_key=None, **params):
        headers = {}
        return self.request('post', self['url'], params, headers)

    def retrieve(self, id, **params):
        base = self.get('url')
        id = util.utf8(id)
        extn = urllib.quote_plus(id)
        url = "%s/%s" % (base, extn)

        return self.request('get', url, params)

    def __iter__(self):
        return getattr(self, 'data', []).__iter__()


class SingletonAPIResource(APIResource):

    @classmethod
    def retrieve(cls, **params):
        return super(SingletonAPIResource, cls).retrieve(None, **params)

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "/v1/%s" % (cls_name,)

    def instance_url(self):
        return self.class_url()


# Classes of API operations
class ListableAPIResource(APIResource):

    @classmethod
    def all(cls, *args, **params):
        return cls.list(*args, **params)

    @classmethod
    def auto_paging_iter(self, *args, **params):
        return self.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(cls, api_key=None, idempotency_key=None, **params):
        requester = api_requester.APIRequester(api_key,
                                               api_base=cls.api_base())
        url = cls.class_url()
        response, api_key = requester.request('get', url, params)
        ap_object = convert_to_ap_object(response, api_key)
        ap_object._retrieve_params = params
        return ap_object


class CreateableAPIResource(APIResource):

    @classmethod
    def create(cls, api_key=None, idempotency_key=None, **params):
        requester = api_requester.APIRequester(api_key)
        url = cls.class_url()
        headers = {}
        response, api_key = requester.request('post', url, params, headers)
        return convert_to_ap_object(response, api_key)


class UpdateableAPIResource(APIResource):

    @classmethod
    def _modify(cls, url, api_key=None, idempotency_key=None, **params):
        requester = api_requester.APIRequester(api_key)
        headers = {}
        response, api_key = requester.request('post', url, params, headers)
        return convert_to_ap_object(response, api_key)

    @classmethod
    def modify(cls, sid, **params):
        url = "%s/%s" % (cls.class_url(), urllib.quote_plus(util.utf8(sid)))
        return cls._modify(url, **params)

class DeletableAPIResource(APIResource):

    def delete(self, **params):
        self.request('delete', self.instance_url(), params)
        return self


# API objects
class Customer(CreateableAPIResource, UpdateableAPIResource,
               ListableAPIResource, DeletableAPIResource):
    pass