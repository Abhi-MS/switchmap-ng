#!/usr/bin/env python3
"""Test the l1interface module."""

import os
import sys
import unittest
import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}switchmap-ng{0}tests{0}switchmap_{0}db{0}table'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)


# Create the necessary configuration to load the module
from tests.testlib_ import setup
CONFIG = setup.config()
CONFIG.save()

from switchmap.db.table import l1interface as testimport
from switchmap.db.table import event
from switchmap.db.table import zone
from switchmap.db.table import device
from switchmap.db.models import L1Interface
from switchmap.db.table import RL1Interface
from switchmap.db.table import IL1Interface
from switchmap.db.table import IEvent
from switchmap.db.table import IZone
from switchmap.db.table import IDevice
from switchmap.db import models

from tests.testlib_ import db
from tests.testlib_ import data


class TestDbTableL1interface(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    @classmethod
    def setUpClass(cls):
        """Steps to execute before tests start."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

        # Create database tables
        models.create_all_tables()

        # Pollinate db with prerequisites
        _prerequisites()

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_idx_exists(self):
        """Testing function idx_exists."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        nonexistent = testimport.exists(row.idx_device, row.ifindex)
        self.assertFalse(nonexistent)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        preliminary_result = testimport.exists(row.idx_device, row.ifindex)
        self.assertTrue(preliminary_result)
        self.assertEqual(_convert(preliminary_result), _convert(row))

        # Test idx_index function
        result = testimport.idx_exists(preliminary_result.idx_l1interface)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(preliminary_result))

    def test_exists(self):
        """Testing function exists."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.idx_device, row.ifindex)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.idx_device, row.ifindex)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_insert_row(self):
        """Testing function insert_row."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.idx_device, row.ifindex)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.idx_device, row.ifindex)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_update_row(self):
        """Testing function update_row."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.idx_device, row.ifindex)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.idx_device, row.ifindex)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

        # Do an update
        idx = result.idx_l1interface
        updated_row = L1Interface(
            idx_device=row.idx_device,
            ifindex=row.ifindex,
            duplex=row.duplex,
            ethernet=row.ethernet,
            nativevlan=row.nativevlan,
            trunk=row.trunk,
            ifspeed=row.ifspeed,
            ifalias=row.ifalias,
            ifdescr=data.random_string(),
            ifadminstatus=row.ifadminstatus,
            ifoperstatus=row.ifoperstatus,
            ts_idle=row.ts_idle,
            cdpcachedeviceid=row.cdpcachedeviceid,
            cdpcachedeviceport=row.cdpcachedeviceport,
            cdpcacheplatform=row.cdpcacheplatform,
            lldpremportdesc=row.lldpremsysdesc,
            lldpremsyscapenabled=row.lldpremsyscapenabled,
            lldpremsysdesc=row.lldpremportdesc,
            lldpremsysname=row.lldpremsysname,
            enabled=row.enabled
        )
        testimport.update_row(idx, updated_row)

        # Test the update
        result = testimport.exists(updated_row.idx_device, updated_row.ifindex)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(updated_row))

    def test__row(self):
        """Testing function _row."""
        # This function is tested by all the other tests
        pass


def _convert(row):
    """Convert RL1Interface to IL1Interface record.

    Args:
        row: RL1Interface/IL1Interface record

    Returns:
        result: IL1Interface result

    """
    # Do conversion
    result = IL1Interface(
        idx_device=row.idx_device,
        ifindex=row.ifindex,
        duplex=row.duplex,
        ethernet=row.ethernet,
        nativevlan=row.nativevlan,
        trunk=row.trunk,
        ifspeed=row.ifspeed,
        ifalias=row.ifalias,
        ifdescr=row.ifdescr,
        ifadminstatus=row.ifadminstatus,
        ifoperstatus=row.ifoperstatus,
        ts_idle=row.ts_idle,
        cdpcachedeviceid=row.cdpcachedeviceid,
        cdpcachedeviceport=row.cdpcachedeviceport,
        cdpcacheplatform=row.cdpcacheplatform,
        lldpremportdesc=row.lldpremsysdesc,
        lldpremsyscapenabled=row.lldpremsyscapenabled,
        lldpremsysdesc=row.lldpremportdesc,
        lldpremsysname=row.lldpremsysname,
        enabled=row.enabled
    )
    return result


def _row():
    """Create an IL1Interface record.

    Args:
        None

    Returns:
        result: IL1Interface object

    """
    # Create result
    result = IL1Interface(
        idx_device=1,
        ifindex=random.randint(0, 1000000),
        duplex=random.randint(0, 1000000),
        ethernet=1,
        nativevlan=random.randint(0, 1000000),
        trunk=1,
        ifspeed=random.randint(0, 1000000),
        ifalias=data.random_string(),
        ifdescr=data.random_string(),
        ifadminstatus=random.randint(0, 1000000),
        ifoperstatus=random.randint(0, 1000000),
        ts_idle=random.randint(0, 1000000),
        cdpcachedeviceid=data.random_string(),
        cdpcachedeviceport=data.random_string(),
        cdpcacheplatform=data.random_string(),
        lldpremportdesc=data.random_string(),
        lldpremsyscapenabled=data.random_string(),
        lldpremsysdesc=data.random_string(),
        lldpremsysname=data.random_string(),
        enabled=1
    )
    return result


def _prerequisites():
    """Create prerequisite rows.

    Args:
        None

    Returns:
        None

    """
    # Create result
    event.insert_row(
        IEvent(
            name=data.random_string(),
            enabled=1
            )
    )
    zone.insert_row(
        IZone(
            name=data.random_string(),
            company_name=data.random_string(),
            address_0=data.random_string(),
            address_1=data.random_string(),
            address_2=data.random_string(),
            city=data.random_string(),
            state=data.random_string(),
            country=data.random_string(),
            postal_code=data.random_string(),
            phone=data.random_string(),
            notes=data.random_string(),
            enabled=1
        )
    )
    device.insert_row(
        IDevice(
            idx_zone=1,
            idx_event=1,
            sys_name=data.random_string(),
            hostname=data.random_string(),
            name=data.random_string(),
            sys_description=data.random_string(),
            sys_objectid=data.random_string(),
            sys_uptime=random.randint(0, 1000000),
            last_polled=random.randint(0, 1000000),
            enabled=1
        )
    )


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
