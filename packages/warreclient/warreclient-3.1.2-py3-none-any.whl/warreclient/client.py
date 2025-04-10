#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
from keystoneauth1 import adapter
from nectarclient_lib import exceptions
from oslo_utils import importutils

import warreclient


def Client(version, *args, **kwargs):
    module = f'warreclient.v{version}.client'
    module = importutils.import_module(module)
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)


class SessionClient(adapter.Adapter):
    client_name = 'python-warreclient'
    client_version = warreclient.__version__

    def request(self, url, method, **kwargs):
        kwargs.setdefault('headers', kwargs.get('headers', {}))
        # NOTE(sorrison): The standard call raises errors from
        # keystoneauth, where we need to raise the warreclient errors.
        raise_exc = kwargs.pop('raise_exc', True)
        resp = super().request(url, method, raise_exc=False, **kwargs)

        if raise_exc and resp.status_code >= 400:
            raise exceptions.from_response(resp, url, method)
        # NOTE(sorrison): Deletes don't return json body
        if resp.status_code == 204:
            return resp, '{}'
        return resp, resp.json()
