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
import json
from osc_lib.tests import utils as osctestutils
from unittest import mock

from esileapclient.osc.v1 import lease
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestLease(base.TestESILeapCommand):
    def setUp(self):
        super(TestLease, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()


class TestCreateLease(TestLease):
    def setUp(self):
        super(TestCreateLease, self).setUp()

        self.client_mock.create_lease.return_value = base.FakeResource(
            copy.deepcopy(fakes.LEASE)
        )

        # Get the command object to test
        self.cmd = lease.CreateLease(self.app, None)

    def test_lease_create(self):
        arglist = [
            fakes.lease_resource_uuid,
            fakes.lease_project_id,
            "--end-time",
            fakes.lease_end_time,
            "--name",
            fakes.lease_name,
            "--properties",
            fakes.lease_properties,
            "--resource-type",
            fakes.lease_resource_type,
            "--start-time",
            fakes.lease_start_time,
            "--purpose",
            fakes.lease_purpose,
        ]

        verifylist = [
            ("end_time", fakes.lease_end_time),
            ("name", fakes.lease_name),
            ("project_id", fakes.lease_project_id),
            ("properties", fakes.lease_properties),
            ("resource_type", fakes.lease_resource_type),
            ("resource_uuid", fakes.lease_resource_uuid),
            ("start_time", fakes.lease_start_time),
            ("purpose", fakes.lease_purpose),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        args = {
            "resource_type": fakes.lease_resource_type,
            "resource_uuid": fakes.lease_resource_uuid,
            "project_id": fakes.lease_project_id,
            "end_time": fakes.lease_end_time,
            "name": fakes.lease_name,
            "properties": json.loads(fakes.lease_properties),
            "start_time": fakes.lease_start_time,
            "purpose": fakes.lease_purpose,
        }

        self.client_mock.create_lease.assert_called_once_with(**args)


class TestUpdateLease(TestLease):
    def setUp(self):
        super(TestUpdateLease, self).setUp()
        lease_return = base.FakeResource(copy.deepcopy(fakes.LEASE))
        self.client_mock.update_lease.return_value = dict(lease_return.__dict__)

        # Get the command object to test
        self.cmd = lease.UpdateLease(self.app, None)

    def test_lease_update(self):
        arglist = [
            fakes.lease_uuid,
            "--end-time",
            fakes.lease_end_time,
        ]

        verifylist = [
            ("uuid", fakes.lease_uuid),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.client_mock.update_lease.assert_called_once_with(
            fakes.lease_uuid, end_time=fakes.lease_end_time
        )

    def test_update_show_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(
            osctestutils.ParserException,
            self.check_parser,
            self.cmd,
            arglist,
            verifylist,
        )


class TestLeaseList(TestLease):
    def setUp(self):
        super(TestLeaseList, self).setUp()

        self.client_mock.leases.return_value = [
            base.FakeResource(copy.deepcopy(fakes.LEASE))
        ]
        self.cmd = lease.ListLease(self.app, None)

    def test_lease_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            "status": parsed_args.status,
            "offer_uuid": parsed_args.offer_uuid,
            "start_time": str(parsed_args.time_range[0])
            if parsed_args.time_range
            else None,
            "end_time": str(parsed_args.time_range[1])
            if parsed_args.time_range
            else None,
            "project_id": parsed_args.project_id,
            "owner_id": parsed_args.owner_id,
            "view": "all" if parsed_args.all else None,
            "resource_type": parsed_args.resource_type,
            "resource_uuid": parsed_args.resource_uuid,
            "resource_class": parsed_args.resource_class,
            "purpose": parsed_args.purpose,
        }

        self.client_mock.leases.assert_called_with(**filters)

        collist = [
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

    @mock.patch("esileapclient.common.utils.filter_nodes_by_properties")
    def test_lease_list_with_property_filter(self, mock_filter_nodes):
        arglist = ["--property", "cpus>=40"]
        verifylist = [("properties", ["cpus>=40"])]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            "status": parsed_args.status,
            "offer_uuid": parsed_args.offer_uuid,
            "start_time": str(parsed_args.time_range[0])
            if parsed_args.time_range
            else None,
            "end_time": str(parsed_args.time_range[1])
            if parsed_args.time_range
            else None,
            "project_id": parsed_args.project_id,
            "owner_id": parsed_args.owner_id,
            "view": "all" if parsed_args.all else None,
            "resource_type": parsed_args.resource_type,
            "resource_uuid": parsed_args.resource_uuid,
            "resource_class": parsed_args.resource_class,
            "purpose": parsed_args.purpose,
        }

        self.client_mock.leases.assert_called_with(**filters)
        mock_filter_nodes.assert_called_with(mock.ANY, parsed_args.properties)

    def test_lease_list_long(self):
        arglist = ["--long"]
        verifylist = [("long", True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            "status": parsed_args.status,
            "offer_uuid": parsed_args.offer_uuid,
            "start_time": str(parsed_args.time_range[0])
            if parsed_args.time_range
            else None,
            "end_time": str(parsed_args.time_range[1])
            if parsed_args.time_range
            else None,
            "project_id": parsed_args.project_id,
            "owner_id": parsed_args.owner_id,
            "view": "all" if parsed_args.all else None,
            "resource_type": parsed_args.resource_type,
            "resource_uuid": parsed_args.resource_uuid,
            "resource_class": parsed_args.resource_class,
            "purpose": parsed_args.purpose,
        }

        self.client_mock.leases.assert_called_with(**filters)

        long_collist = [
            "UUID",
            "Resource",
            "Resource Class",
            "Resource Properties",
            "Project",
            "Start Time",
            "End Time",
            "Expire Time",
            "Fulfill Time",
            "Offer UUID",
            "Owner",
            "Parent Lease UUID",
            "Status",
            "Purpose",
        ]

        self.assertEqual(long_collist, list(columns))

        datalist = (
            (
                fakes.lease_uuid,
                fakes.lease_resource,
                fakes.lease_resource_class,
                fakes.node_properties,
                fakes.lease_project,
                fakes.lease_start_time,
                fakes.lease_end_time,
                fakes.lease_expire_time,
                fakes.lease_fulfill_time,
                fakes.offer_uuid,
                fakes.lease_owner,
                fakes.parent_lease_uuid,
                fakes.lease_status,
                fakes.lease_purpose,
            ),
        )
        self.assertEqual(datalist, tuple(data))

    @mock.patch("esileapclient.common.utils.filter_nodes_by_properties")
    def test_lease_list_long_with_property_filter(self, mock_filter_nodes):
        arglist = ["--long", "--property", "memory_mb<=262144"]
        verifylist = [("long", True), ("properties", ["memory_mb<=262144"])]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            "status": parsed_args.status,
            "offer_uuid": parsed_args.offer_uuid,
            "start_time": str(parsed_args.time_range[0])
            if parsed_args.time_range
            else None,
            "end_time": str(parsed_args.time_range[1])
            if parsed_args.time_range
            else None,
            "project_id": parsed_args.project_id,
            "owner_id": parsed_args.owner_id,
            "view": "all" if parsed_args.all else None,
            "resource_type": parsed_args.resource_type,
            "resource_uuid": parsed_args.resource_uuid,
            "resource_class": parsed_args.resource_class,
            "purpose": parsed_args.purpose,
        }

        self.client_mock.leases.assert_called_with(**filters)
        mock_filter_nodes.assert_called_with(mock.ANY, parsed_args.properties)


class TestLeaseShow(TestLease):
    def setUp(self):
        super(TestLeaseShow, self).setUp()

        self.client_mock.get_lease.return_value = base.FakeResource(
            copy.deepcopy(fakes.LEASE)
        )

        self.cmd = lease.ShowLease(self.app, None)

    def test_lease_show(self):
        arglist = [fakes.lease_uuid]
        verifylist = [("uuid", fakes.lease_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.client_mock.get_lease.assert_called_once_with(fakes.lease_uuid)

        collist = (
            "end_time",
            "expire_time",
            "fulfill_time",
            "name",
            "offer_uuid",
            "owner",
            "owner_id",
            "parent_lease_uuid",
            "project",
            "project_id",
            "properties",
            "purpose",
            "resource",
            "resource_class",
            "resource_properties",
            "resource_type",
            "resource_uuid",
            "start_time",
            "status",
            "uuid",
        )

        self.assertEqual(collist, columns)

        datalist = (
            fakes.lease_end_time,
            fakes.lease_expire_time,
            fakes.lease_fulfill_time,
            fakes.lease_name,
            fakes.offer_uuid,
            fakes.lease_owner,
            fakes.lease_owner_id,
            fakes.parent_lease_uuid,
            fakes.lease_project,
            fakes.lease_project_id,
            json.loads(fakes.lease_properties),
            fakes.lease_purpose,
            fakes.lease_resource,
            fakes.lease_resource_class,
            fakes.node_properties,
            fakes.lease_resource_type,
            fakes.lease_resource_uuid,
            fakes.lease_start_time,
            fakes.lease_status,
            fakes.lease_uuid,
        )
        self.assertEqual(datalist, tuple(data))

    def test_lease_show_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(
            osctestutils.ParserException,
            self.check_parser,
            self.cmd,
            arglist,
            verifylist,
        )


class TestLeaseDelete(TestLease):
    def setUp(self):
        super(TestLeaseDelete, self).setUp()

        self.cmd = lease.DeleteLease(self.app, None)

    def test_lease_delete(self):
        arglist = [fakes.lease_uuid]
        verifylist = [("uuid", fakes.lease_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.client_mock.delete_lease.assert_called_once_with(fakes.lease_uuid)

    def test_lease_delete_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(
            osctestutils.ParserException,
            self.check_parser,
            self.cmd,
            arglist,
            verifylist,
        )
