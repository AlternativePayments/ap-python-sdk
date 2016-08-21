import sys
import urllib

from ap_python_sdk import api_requester, util


def convert_to_ap_object(resp, class_url):
    types = {
        '/customers': Customer
    }

    if isinstance(resp, list):
        return [convert_to_ap_object(i, class_url) for i in resp]
    elif isinstance(resp, dict) and not isinstance(resp, BaseModel):
        resp = resp.copy()
        klass = types.get(class_url, BaseModel)
        return klass.construct_from(resp)
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

class BaseModel(dict):
    def __init__(self, **params):
        super(BaseModel, self).__init__()

        for k, v in params.iteritems():
            self.__setitem__(k, v)

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

    def __getitem__(self, k):
        try:
            return super(BaseModel, self).__getitem__(k)
        except KeyError as err:
            raise err

    def __delitem__(self, k):
        super(BaseModel, self).__delitem__(k)

    @classmethod
    def construct_from(cls, values):
        instance = cls(**values)
        return instance

    @classmethod
    def api_base(cls):
        return None

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

class Pagination(BaseModel):
    pass

class Collection(dict):

    def __init__(self, params):
        super(Collection, self).__init__()

        for k, v in params.iteritems():
            self.__setitem__(k, v)

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        super(Collection, self).__setitem__(k, v)

    # TODO: Fix to create object of Pagination.
    def pagination(self, pagination):
        self.pagination = Pagination(pagination)

class APIResource(BaseModel):

    @classmethod
    def class_url(cls):
        raise NotImplementedError(
                'APIResource is an abstract class.  You should perform '
                'actions on its subclasses (e.g. Customer)')

    @classmethod
    def list_members(cls):
        raise NotImplementedError('APIResource is an abstract class.'
                                ' You should use it\'s subclasses (Customer, Payment, etc.)')

# Classes of API operations
class ListableAPIResource(APIResource):

    @classmethod
    def all(cls, api_key=None, **pagination_options):
        requester = api_requester.APIRequester(api_key)
        class_url = cls.class_url()
        url = '%s/' % class_url

        response = requester.request('get', url, pagination_options)
        list = convert_to_ap_object(response[cls.list_members()], class_url)
        return Collection({
                           'items': list,
                           'pagination': response['pagination']
        })


class CreateableAPIResource(APIResource):

    @classmethod
    def create(cls, params={}, api_key=None):
        requester = api_requester.APIRequester(api_key)
        url = cls.class_url()
        headers = {}
        response = requester.request('post', url, params, headers)

        return convert_to_ap_object(response, url)

class RetrivableAPIResource(APIResource):

    @classmethod
    def retrieve(self, id, params={}, api_key=None):
        requester = api_requester.APIRequester(api_key)
        class_url = self.class_url()
        headers = {}

        url = "%s/%s" % (class_url, id)

        response = requester.request('get', url, params, headers)
        return convert_to_ap_object(response, class_url)

# API objects
class Customer(CreateableAPIResource, ListableAPIResource, RetrivableAPIResource):

    @classmethod
    def class_url(cls):
        return '/customers'

    @classmethod
    def list_members(cls):
        return 'customers'