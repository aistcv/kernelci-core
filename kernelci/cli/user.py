# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Copyright (C) 2023 Collabora Limited
# Author: Guillaume Tucker <guillaume.tucker@collabora.com>

"""Tool to manage KernelCI API users"""

import getpass

from .base import Args, sub_main
from .base_api import APICommand, AttributesCommand


class cmd_whoami(APICommand):  # pylint: disable=invalid-name
    """Use the /whoami entry point to get the current user's data"""
    args = APICommand.args + [Args.api_token]
    opt_args = APICommand.opt_args + [Args.indent]

    def _api_call(self, api, configs, args):
        data = api.whoami()
        self._print_json(data, args.indent)
        return True


class cmd_get_token(APICommand):  # pylint: disable=invalid-name
    """Create a new API token for the current user"""
    args = APICommand.args + [Args.username]
    opt_args = APICommand.opt_args + [
        {
            'name': '--scopes',
            'action': 'append',
            'help': "Security scopes",
        },
    ]

    def _api_call(self, api, configs, args):
        password = getpass.getpass()
        token = api.create_token(args.username, password, args.scopes)
        self._print_json(token, args.indent)
        return True


class cmd_password_hash(APICommand):  # pylint: disable=invalid-name
    """Get an encryption hash for an arbitrary password"""

    def _api_call(self, api, configs, args):
        password = getpass.getpass()
        print(api.password_hash(password))
        return True


class cmd_get_group(APICommand):  # pylint: disable=invalid-name
    """Get a user group with a given ID"""
    args = APICommand.args + [Args.group_id]
    opt_args = APICommand.opt_args + [Args.indent]

    def _api_call(self, api, configs, args):
        group = api.get_group(args.group_id)
        self._print_json(group, args.indent)
        return True


class cmd_find_groups(AttributesCommand):  # pylint: disable=invalid-name
    """Find user groups with arbitrary attributes"""
    opt_args = AttributesCommand.opt_args + [
        {
            'name': '--limit',
            'type': int,
            'help': """\
Maximum number of groups to retrieve. When set to 0, no limit is used and all
the matching groups are retrieved.\
""",
            'default': 10,
        },
        {
            'name': '--offset',
            'type': int,
            'help': "Offset when paginating results with a number of groups",
        },
    ]

    def _api_call(self, api, configs, args):
        attributes = self._split_attributes(args.attributes)
        groups = api.get_groups(attributes, args.offset, args.limit)
        self._print_json(groups, args.indent)
        return True


def main(args=None):
    """Entry point for the command line tool"""
    sub_main("user", globals(), args)
