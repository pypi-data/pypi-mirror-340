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

import copy
import mock

from esi import connection

from esileapclient.osc.v1.mdc import mdc_lease
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestMDCLease(base.TestESILeapCommand):
    def setUp(self):
        super(TestMDCLease, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()


class TestMDCLeaseList(TestMDCLease):
    def setUp(self):
        super(TestMDCLeaseList, self).setUp()

        class FakeCloudRegion(object):
            def __init__(self, name, region):
                self.name = name
                self.config = {"region_name": region}

            def get_session(self):
                return None

        self.cloud1 = FakeCloudRegion("cloud1", "regionOne")
        self.cloud2 = FakeCloudRegion("cloud2", "regionTwo")
        self.lease1 = base.FakeResource(copy.deepcopy(fakes.LEASE))
        self.lease2 = base.FakeResource(copy.deepcopy(fakes.LEASE))
        self.cmd = mdc_lease.MDCListLease(self.app, None)

    @mock.patch("openstack.config.loader.OpenStackConfig.get_all_clouds")
    @mock.patch.object(connection, "ESIConnection")
    def test_mdc_lease_list(self, mock_conn, mock_clouds):
        mock_clouds.return_value = [self.cloud1, self.cloud2]
        mock_conn.return_value.lease = self.client_mock
        self.client_mock.leases.side_effect = [[self.lease1], [self.lease2]]

        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            "status": parsed_args.status,
            "start_time": str(parsed_args.time_range[0])
            if parsed_args.time_range
            else None,
            "end_time": str(parsed_args.time_range[1])
            if parsed_args.time_range
            else None,
            "resource_type": parsed_args.resource_type,
            "resource_class": parsed_args.resource_class,
            "purpose": parsed_args.purpose,
        }
        self.client_mock.leases.assert_called_with(**filters)

        collist = [
            "Cloud",
            "Region",
            "UUID",
            "Resource",
            "Resource Class",
            "Project",
            "Start Time",
            "End Time",
            "Offer UUID",
            "Status",
            "Purpose",
        ]

        self.assertEqual(collist, list(columns))

        datalist = (
            (
                "cloud1",
                "regionOne",
                fakes.lease_uuid,
                fakes.lease_resource,
                fakes.lease_resource_class,
                fakes.lease_project,
                fakes.lease_start_time,
                fakes.lease_end_time,
                fakes.offer_uuid,
                fakes.lease_status,
                fakes.lease_purpose,
            ),
            (
                "cloud2",
                "regionTwo",
                fakes.lease_uuid,
                fakes.lease_resource,
                fakes.lease_resource_class,
                fakes.lease_project,
                fakes.lease_start_time,
                fakes.lease_end_time,
                fakes.offer_uuid,
                fakes.lease_status,
                fakes.lease_purpose,
            ),
        )
        self.assertEqual(datalist, tuple(data))

    @mock.patch("openstack.config.loader.OpenStackConfig.get_all_clouds")
    @mock.patch.object(connection, "ESIConnection")
    def test_mdc_lease_list_filter(self, mock_conn, mock_clouds):
        mock_clouds.return_value = [self.cloud1, self.cloud2]
        mock_conn.return_value.lease = self.client_mock
        self.client_mock.leases.return_value = [self.lease2]

        arglist = ["--clouds", "cloud2"]
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            "status": parsed_args.status,
            "start_time": str(parsed_args.time_range[0])
            if parsed_args.time_range
            else None,
            "end_time": str(parsed_args.time_range[1])
            if parsed_args.time_range
            else None,
            "resource_type": parsed_args.resource_type,
            "resource_class": parsed_args.resource_class,
            "purpose": parsed_args.purpose,
        }

        self.client_mock.leases.assert_called_with(**filters)

        collist = [
            "Cloud",
            "Region",
            "UUID",
            "Resource",
            "Resource Class",
            "Project",
            "Start Time",
            "End Time",
            "Offer UUID",
            "Status",
            "Purpose",
        ]

        self.assertEqual(collist, list(columns))

        datalist = (
            (
                "cloud2",
                "regionTwo",
                fakes.lease_uuid,
                fakes.lease_resource,
                fakes.lease_resource_class,
                fakes.lease_project,
                fakes.lease_start_time,
                fakes.lease_end_time,
                fakes.offer_uuid,
                fakes.lease_status,
                fakes.lease_purpose,
            ),
        )
        self.assertEqual(datalist, tuple(data))
