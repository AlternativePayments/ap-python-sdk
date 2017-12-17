from __builtin__ import classmethod
from ap_python_sdk import api_requester, util, api_public_key as globaly_defined_api_public_key
import sys


def convert_to_ap_object(resp, class_url):
    types = {
        '/customers': Customer,
        '/preauthorizations': Preauthorization,
        '/phoneverification': PhoneVerification,
        '/websites': Website,
        '/paymentoptions': PaymentOption,
        '/transactions': Transaction,
        '/transactions/hosted': HostedTransaction,
        '/plans': Plan,
        '/subscriptions': Subscription,
        '/voids': Void,
        '/refunds': Refund
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

        if getattr(self, k, None) != None:
            getattr(self, k)(**v)
        else:
            super(BaseModel, self).__setitem__(k, v)

    @classmethod
    def construct_from(cls, values):
        instance = cls(**values)
        return instance

    @classmethod
    def api_base(cls):
        return None

    @classmethod
    def url_with_prefix(cls, url_prefix):
        if url_prefix != None:
            return '%s%s' % (url_prefix, cls.class_url())
        else:
            return cls.class_url()

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
        temp_dict = dict(self, **self.__dict__)

        return util.json.dumps(temp_dict, sort_keys=True, indent=2)

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

        # We need items condition here as dictionary has builtin items() method.
        if k != 'items' and getattr(self, k, None) != None:
            getattr(self, k)(**v)
        else:
            super(Collection, self).__setitem__(k, v)

    def pagination(self, **pagination):
        self.pagination = Pagination(**pagination)

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
    def all(cls, api_secret_key=None, api_public_key=None, url_prefix=None, **pagination_options):
        requester = api_requester.APIRequester(api_secret_key, api_public_key)

        response = requester.request('get', '%s/' % cls.url_with_prefix(url_prefix), pagination_options)
        list_objects = convert_to_ap_object(response[cls.list_members()], cls.class_url())
        return Collection({
                           'items': list_objects,
                           'pagination': response.get('pagination', {})
        })


class CreateableAPIResource(APIResource):

    @classmethod
    def create(cls, params={}, url_prefix=None, api_secret_key=None, api_public_key=None):
        requester = api_requester.APIRequester(api_secret_key, api_public_key)
        headers = {}
        response = requester.request('post', cls.url_with_prefix(url_prefix), params, headers)

        return convert_to_ap_object(response, cls.class_url())

class RetrivableAPIResource(APIResource):

    @classmethod
    def retrieve(self, id, params={}, url_prefix=None, api_secret_key=None, api_public_key=None):
        requester = api_requester.APIRequester(api_secret_key, api_public_key)
        headers = {}
        response = requester.request('get', "%s/%s" % (self.url_with_prefix(url_prefix), id), params, headers)

        return convert_to_ap_object(response, self.class_url())

class CreatePhoneVerificationAPIResource(APIResource):
    
    @classmethod
    def create_phone_verification(cls, params={}, url_prefix=None, api_secret_key=None, api_public_key=None):
        api_public_key = api_public_key or globaly_defined_api_public_key

        params['key'] = api_public_key
        requester = api_requester.APIRequester(api_secret_key, api_public_key)
        headers = {}
        response = requester.request('post', cls.url_with_prefix(url_prefix), params, headers)

        return convert_to_ap_object(response, cls.class_url())

# API objects
class Customer(CreateableAPIResource, ListableAPIResource, RetrivableAPIResource):

    @classmethod
    def class_url(cls):
        return '/customers'

    @classmethod
    def list_members(cls):
        return 'customers'

class Payment(BaseModel):
    pass

class PaymentOption(RetrivableAPIResource):

    @classmethod
    def class_url(cls):
        return '/paymentoptions'

    @classmethod
    def list_members(cls):
        return 'paymentoptions'

class Website(RetrivableAPIResource):

    @classmethod
    def class_url(cls):
        return '/websites'

    @classmethod
    def is_phone_verification_on(cls, payment_option=None):
        return PaymentOption.retrieve(payment_option, {}, '%s/%s' % (cls.class_url(), globaly_defined_api_public_key))

class RedirectUrls(BaseModel):
    pass

class Preauthorization(CreateableAPIResource, RetrivableAPIResource):

    @classmethod
    def class_url(cls):
        return '/preauthorizations'

    @classmethod
    def list_members(cls):
        return 'preauthorizations'

    def customer(self, **customer):
        self.customer = Customer(**customer)

    def payment(self, **payment):
        self.payment = Payment(**payment)

class PhoneVerification(CreateableAPIResource, CreatePhoneVerificationAPIResource, RetrivableAPIResource):

    @classmethod
    def class_url(cls):
        return '/phoneverification'

class Transaction(CreateableAPIResource, ListableAPIResource, RetrivableAPIResource):

    @classmethod
    def class_url(cls):
        return '/transactions'

    @classmethod
    def list_members(cls):
        return 'transactions'

    @classmethod
    def void(self, reason='', transaction_id=None):
        if transaction_id == None:
            transaction_id = self.id

        return Void.create({'reason': reason}, '%s/%s' % (self.class_url(), transaction_id))

    @classmethod
    def retrieve_void(self, void_id=None, transaction_id=None):
        if transaction_id == None:
            transaction_id = self.id

        return Void.retrieve(void_id, {}, '%s/%s' % (self.class_url(), transaction_id))

    @classmethod
    def voids(self, transaction_id=None):
        if transaction_id == None:
            transaction_id = self.id

        return Void.all(url_prefix='%s/%s' % (self.class_url(), transaction_id))

    @classmethod
    def refund(self, reason='', transaction_id=None):
        if transaction_id == None:
            transaction_id = self.id

        return Refund.create({'reason': reason}, '%s/%s' % (self.class_url(), transaction_id))

    @classmethod
    def retrieve_refund(self, refund_id=None, transaction_id=None):
        if transaction_id == None:
            transaction_id = self.id

        return Refund.retrieve(refund_id, {}, '%s/%s' % (self.class_url(), transaction_id))

    @classmethod
    def refunds(self, transaction_id=None):
        if transaction_id == None:
            transaction_id = self.id

        return Refund.all(url_prefix='%s/%s' % (self.class_url(), transaction_id))

    def customer(self, **customer):
        self.customer = Customer(**customer)

    def payment(self, **payment):
        self.payment = Payment(**payment)

    def redirectUrls(self, **redirectUrls):
        self.redirectUrls = RedirectUrls(**redirectUrls)

    def phoneverification(self, **phoneverification):
        self.phoneverification = PhoneVerification(**phoneverification)

class HostedTransaction(Transaction):
    
    @classmethod
    def class_url(cls):
        return '/transactions/hosted'

    @classmethod
    def list_members(cls):
        return 'transactions'

class Plan(CreateableAPIResource, RetrivableAPIResource, ListableAPIResource):

    @classmethod
    def class_url(cls):
        return '/plans'

    @classmethod
    def list_members(cls):
        return 'plans'

class Subscription(CreateableAPIResource, RetrivableAPIResource, ListableAPIResource):

    @classmethod
    def class_url(cls):
        return '/subscriptions'

    @classmethod
    def list_members(cls):
        return 'subscriptions'

    def customer(self, **customer):
        self.customer = Customer(**customer)

    def payment(self, **payment):
        self.payment = Payment(**payment)

    def plan(self, **plan):
        self.plan = Plan(**plan)

class Void(CreateableAPIResource, RetrivableAPIResource, ListableAPIResource):

    @classmethod
    def class_url(cls):
        return '/voids'

    @classmethod
    def list_members(cls):
        return 'voidTransactions'

    def originalTransaction(self, **originalTransaction):
        self.originalTransaction = Transaction(**originalTransaction)

class Refund(CreateableAPIResource, RetrivableAPIResource, ListableAPIResource):

    @classmethod
    def class_url(cls):
        return '/refunds'

    @classmethod
    def list_members(cls):
        return 'refundTransactions'

    def originalTransaction(self, **originalTransaction):
        self.originalTransaction = Transaction(**originalTransaction)

# Enumeration classes
class Period(dict):

    DAY = 'Day'
    WEEK = 'Week'
    MONTH = 'Month'
    YEAR = 'Year'

class RefundReason:

    CHARGEBACK_AVOIDANCE = 'CHARGEBACK_AVOIDANCE'
    END_USER_ERROR = 'END_USER_ERROR'
    FRAUD = 'FRAUD'
    UNSATISFIED_CUSTOMER = 'UNSATISFIED_CUSTOMER'
    INVALID_TRANSACTION = 'INVALID_TRANSACTION'
