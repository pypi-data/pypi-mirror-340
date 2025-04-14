# This file is part of the Open Data Cube, see https://opendatacube.org for more information
#
# Copyright (c) 2015-2025 ODC Contributors
# SPDX-License-Identifier: Apache-2.0
import logging
from typing import Any
from collections.abc import Iterable

_LOG = logging.getLogger(__name__)


def load_drivers(group: str) -> dict[str, Any]:
    """
    Load available drivers for a given group name.

    Gracefully handles:

     - Driver module not able to be imported
     - Driver init function throwing an exception or returning None

     By having driver entry_points pointing to a function, we defer loading the driver
     module or running any code until required.

    :param group: Name of the entry point group e.g. "datacube.plugins.io.read"

    :returns: Dictionary String -> Driver Object
    """

    def safe_load(ep):
        # pylint: disable=broad-except,bare-except
        try:
            driver_init = ep.load()
        except Exception as e:
            _LOG.warning('Failed to resolve driver %s::%s', group, ep.name)
            _LOG.warning('Error was: %s', repr(e))
            return None

        try:
            driver = driver_init()
        except Exception:
            _LOG.warning('Exception during driver init, driver name: %s::%s', group, ep.name)
            return None

        if driver is None:
            _LOG.warning('Driver init returned None, driver name: %s::%s', group, ep.name)

        return driver

    def resolve_all(group: str) -> Iterable[tuple[str, Any]]:
        from importlib.metadata import entry_points
        for ep in entry_points(group=group):
            driver = safe_load(ep)
            if driver is not None:
                yield ep.name, driver

    return dict((name, driver) for name, driver in resolve_all(group))
