#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json


lease_availabilities = "[]"
lease_end_time = "3000-00-00T13"
lease_expire_time = "3000-00-00T13"
lease_owner = "owner-project"
lease_owner_id = "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
lease_project = "lease-project"
lease_project_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
lease_properties = "{}"
lease_resource = "dummy-node-1213123123"
lease_resource_type = "dummy_node"
lease_resource_uuid = "1213123123"
lease_resource_class = "baremetal"
lease_start_time = "2010"
lease_fulfill_time = "2010"
lease_status = "fake_status"
lease_uuid = "9999999"
lease_purpose = "fake_purpose"
offer_uuid = "111111111"
offer_lessee = "lease-project"
offer_lessee_id = "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz"
offer_name = "o1"
parent_lease_uuid = "parent-lease-uuid"
lease_name = "c1"
node_name = "fake-node"
node_uuid = "fake-uuid"
node_owner = "fake-owner"
event_id = 7
event_type = "fake.event"
event_time = "3000-07-01T12"
object_type = "lease"
token_ttl = "60"
node_properties = {
    "cpus": "40",
    "memory_mb": "131072",
    "local_gb": "1200",
    "cpu_arch": "x86_64",
    "vendor": "fake-vendor",
    "cpu_model_name": "fake-model",
    "cpu_frequency": "2000.0",
    "traits": ["trait1", "trait2"],
}

OFFER = {
    "availabilities": json.loads(lease_availabilities),
    "end_time": lease_end_time,
    "lessee": offer_lessee,
    "lessee_id": offer_lessee_id,
    "name": offer_name,
    "parent_lease_uuid": parent_lease_uuid,
    "project": lease_project,
    "project_id": lease_project_id,
    "properties": json.loads(lease_properties),
    "resource": lease_resource,
    "resource_properties": node_properties,
    "resource_type": lease_resource_type,
    "resource_uuid": lease_resource_uuid,
    "resource_class": lease_resource_class,
    "start_time": lease_start_time,
    "status": lease_status,
    "uuid": offer_uuid,
}

LEASE = {
    "end_time": lease_end_time,
    "expire_time": lease_expire_time,
    "fulfill_time": lease_fulfill_time,
    "name": lease_name,
    "offer_uuid": offer_uuid,
    "parent_lease_uuid": parent_lease_uuid,
    "project": lease_project,
    "project_id": lease_project_id,
    "owner": lease_owner,
    "owner_id": lease_owner_id,
    "properties": json.loads(lease_properties),
    "resource": lease_resource,
    "resource_properties": node_properties,
    "resource_type": lease_resource_type,
    "resource_uuid": lease_resource_uuid,
    "resource_class": lease_resource_class,
    "start_time": lease_start_time,
    "status": lease_status,
    "uuid": lease_uuid,
    "purpose": lease_purpose,
}

NODE = {
    "name": node_name,
    "uuid": node_uuid,
    "owner": node_owner,
    "resource_class": lease_resource_class,
    "properties": node_properties,
}

EVENT = {
    "id": event_id,
    "event_type": event_type,
    "event_time": event_time,
    "object_type": object_type,
    "object_uuid": lease_uuid,
    "resource_type": lease_resource_type,
    "resource_uuid": lease_resource_uuid,
    "lessee_id": lease_project_id,
    "owner_id": lease_owner_id,
}

CONSOLE_AUTH_TOKEN = {
    "node_uuid": node_uuid,
}
