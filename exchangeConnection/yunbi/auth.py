import hmac
import hashlib
import time
import urllib

class Auth():
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def urlencode(self, params):
        keys = params.keys()
        keys = sorted(keys)
        query = ''
        for key in keys:
            value = params[key]
            if key != "orders":
                query = "%s&%s=%s" % (query, key, value) if len(query) else "%s=%s" % (key, value)
            else:
                #this ugly code is for multi orders API, there should be an elegant way to do this
                d = {key: params[key]}
                for v in value:
                    ks = v.keys()
                    ks.sort()
                    for k in ks:
                        item = "orders[][%s]=%s" % (k, v[k])
                        query = "%s&%s" % (query, item) if len(query) else "%s" % item
        return query

    def sign(self, verb, path, params=None):
        query = self.urlencode(params)
        msg = "|".join([verb, path, query])
        #
        payload = msg.encode(encoding='UTF8')
        secret_key = self.secret_key.encode(encoding='UTF8')
        signature = hmac.new(secret_key, msg=payload, digestmod=hashlib.sha256).hexdigest()

        #signature = hmac.new(self.secret_key, msg=msg, digestmod=hashlib.sha256).hexdigest()
        return signature

    def sign_params(self, verb, path, params=None):
        if not params:
            params = {}
        params.update({'tonce': int(1000*time.time()), 'access_key': self.access_key})
        query = self.urlencode(params)
        signature = self.sign(verb, path, params)
        return signature, query

    # def createSign(pParams, method, host_url, request_path, secret_key):
    #     sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    #     encode_params = urllib.parse.urlencode(sorted_params)
    #     payload = [method, host_url, request_path, encode_params]
    #     payload = '\n'.join(payload)
    #     payload = payload.encode(encoding='UTF8')
    #     secret_key = secret_key.encode(encoding='UTF8')
    #     digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    #     signature = base64.b64encode(digest)
    #     signature = signature.decode()
    #     return signature