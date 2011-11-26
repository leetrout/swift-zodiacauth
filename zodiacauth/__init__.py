import datetime

from swift.common.client import ClientException
from swift.common.direct_client import direct_head_container, direct_head_object
from swift.common.utils import get_logger, get_remote_client, split_path

from swauth.middleware import json, Swauth

from .utils import zodiac_acl_from_json, zodiac_sign, zodiac_sign_datetime


class ZodiacAuth(Swauth):
    """
    Swift authentication middleware based on swauth that uses the signs of the
    zodiac combined with the remote address to authorize and authenticate.

    Sign and remote address combinations are provided via a JSON file and
    passed to this class via a pastedeploy filter config section.
    """
    def __init__(self, app, conf):
        super(ZodiacAuth, self).__init__(app, conf)
        # set log route to zodiacauth
        self.logger = get_logger(conf, log_route='zodiacauth')
        
        # set our zodiac acl based on a json config
        if 'zodiac_acl_path' in conf:
            zodiac_json = json.loads(open(conf['zodiac_acl_path']).read())
            self.zodiac_acl = zodiac_acl_from_json(zodiac_json)
        else:
            self.zodiac_acl = {}
    
    def __call__(self, environ, start_response):
        #environ['swift.authorize'] = self.authorize
        return super(ZodiacAuth, self).__call__(environ, start_response)
    
    def authorize(self, req):
        ret = super(ZodiacAuth, self).authorize(req)
        if ret is None and req.method == 'GET':
            # passed swauth rules, now check zodiac rules
            
            # split the path
            # this should be safe since it was already checked against an error
            # in the super call
            version, account, container, obj = split_path(req.path, 1, 4, True)
            
            # grab our acl to use
            acl = self.zodiac_acl

            # get the current zodiac sign for this access request
            access_sign = zodiac_sign_datetime(datetime.datetime.now())

            # get the client ip
            client_addr = get_remote_client(req)
            
            if container:
                # there is a container so let's try to get the timestamp
                container_nodes = self.app.container_ring.get_nodes(account, 
                    container)
                if container_nodes:
                    # direct head requests return a timestamp whereas calls
                    # to the proxy do not. this might not be the best thing
                    # to do. open to suggestions.
                    try:
                        container_meta = direct_head_container(
                            container_nodes[1][0],
                            container_nodes[0],
                            account,
                            container
                        )
                    except ClientException:
                        return ret
                    container_date = datetime.datetime.fromtimestamp(
                        float(container_meta['x-timestamp'])
                    )
                    container_sign = zodiac_sign_datetime(container_date)

                    # ensure the container sign has access rules
                    if container_sign in acl and access_sign in \
                    acl[container_sign]:
                        if client_addr not in acl[container_sign][access_sign]:
                            ret = self.denied_response(req)
                    else:
                        # sign missing from acl rules or access sign not present
                        ret = self.denied_response(req)
                    
                    if ret is None and obj:
                        # we passed the container permissions and there is an
                        # object.
                        # get the object's store sign and check permissions
                        obj_nodes = self.app.container_ring.get_nodes(account, 
                            container, obj)
                        if obj_nodes:
                            try:
                                obj_meta = direct_head_object(
                                    obj_nodes[1][0],
                                    container_nodes[0],
                                    account,
                                    container,
                                    obj,
                                )
                            except ClientException:
                                return ret
                            obj_date = datetime.datetime.fromtimestamp(
                                float(obj_meta['x-timestamp'])
                            )
                            obj_sign = zodiac_sign_datetime(obj_date)
                            
                            # ensure the object sign has access rules
                            if obj_sign in acl and access_sign in \
                            acl[obj_sign]:
                                if client_addr not in \
                                acl[obj_sign][access_sign]:
                                    ret = self.denied_response(req)
                            else:
                                # object sign missing from acl rules or 
                                # access sign not present
                                ret = self.denied_response(req)
        return ret


def filter_factory(global_conf, **local_conf):
    """
    Returns a WSGI filter app for use with paste.deploy.
    """
    conf = global_conf.copy()
    conf.update(local_conf)

    def auth_filter(app):
        return ZodiacAuth(app, conf)
    
    return auth_filter
