# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations

"""
"""

import datetime
import errno
import json
import logging
import os

from dciqueue import lib

log = logging.getLogger(__name__)

COMMAND = "remove-resource"


def register_command(subparsers):
    parser = subparsers.add_parser(COMMAND, help="Remove a resource from a pool")
    parser.add_argument("pool", help="Name of the pool")
    parser.add_argument("name", help="Name of the resource")
    parser.add_argument("reason", help="Reason of the removal")
    return COMMAND


def execute_command(args):
    if not lib.check_pool(args):
        return 1

    for key in ("available", "pool"):
        path = os.path.join(args.top_dir, key, args.pool, args.name)
        if os.path.exists(path) or os.path.islink(path):
            log.debug("Removing %s (%s)" % (path, args.reason))
            os.unlink(path)

    dir = os.path.join(args.top_dir, "reason", args.pool)
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise

    path = os.path.join(args.top_dir, "reason", args.pool, args.name)
    with open(path, "w") as f:
        json.dump(
            {
                "reason": args.reason,
                "pool": args.pool,
                "resource": args.name,
                "date": str(datetime.datetime.now()),
            },
            f,
        )

    return 0


# remove_resource_cmd.py ends here
