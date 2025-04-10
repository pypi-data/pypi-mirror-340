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

import datetime

from nectarclient_lib import base


class Flavor(base.Resource):
    date_fields = ['start', 'end']

    def __repr__(self):
        return f"<Flavor {self.id}>"


class FlavorManager(base.BasicManager):
    base_url = 'v1/flavors'
    resource_class = Flavor

    def update(self, flavor_id, **kwargs):
        return self._update(f'/{self.base_url}/{flavor_id}/', data=kwargs)

    def delete(self, flavor_id):
        return self._delete(f'/{self.base_url}/{flavor_id}/')

    def free_slots(self, flavor_id, start=None, end=None):
        today = datetime.date.today()
        if isinstance(start, str):
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        if isinstance(end, str):
            end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        params = {}
        if start is not None:
            params['start'] = start
        if end is None:
            params['end'] = (start or today) + datetime.timedelta(days=30)
        else:
            params['end'] = end
        return self._list(
            f'/{self.base_url}/{flavor_id}/freeslots/',
            obj_class=None,
            raw=True,
            params=params,
        )

    def create(
        self,
        name,
        vcpu,
        memory_mb,
        disk_gb,
        ephemeral_gb=0,
        description=None,
        active=True,
        properties=None,
        max_length_hours=504,
        slots=1,
        is_public=True,
        extra_specs={},
        start=None,
        end=None,
        category=None,
        availability_zone=None,
    ):
        data = {
            'name': name,
            'description': description,
            'vcpu': int(vcpu),
            'memory_mb': int(memory_mb),
            'disk_gb': int(disk_gb),
            'ephemeral_gb': int(ephemeral_gb),
            'properties': properties,
            'active': active,
            'max_length_hours': int(max_length_hours),
            'slots': int(slots),
            'is_public': is_public,
            'extra_specs': extra_specs,
            'start': start,
            'end': end,
            'category': category,
            'availability_zone': availability_zone,
        }

        return self._create(f"/{self.base_url}/", data=data)
