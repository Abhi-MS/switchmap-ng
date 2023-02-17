"""switchmap.classes that manage various configurations."""

import os.path
import os

from switchmap.core.configuration import ConfigCore
from switchmap.core import log
from switchmap.core import files


class ConfigPoller(ConfigCore):
    """Class gathers all configuration information."""

    def __init__(self):
        """Intialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate sub class
        ConfigCore.__init__(self)

        # Initialize key variables
        section = "poller"
        self._config_poller = self._config_complete.get(section)

        # Error if incorrectly configured
        if bool(self._config_poller) is False:
            log_message = (
                'No "{}:" section found in the configuration file(s)'.format(
                    section
                )
            )
            log.log2die_safe(1007, log_message)

    def cache_directory(self):
        """Determine the cache_directory.

        Args:
            None

        Returns:
            result: configured cache_directory

        """
        # Get result
        result = self._config_core.get(
            "cache_directory",
            "{}{}cache".format(self.system_directory(), os.sep),
        )

        # Create the directory if not found
        if os.path.isdir(result) is False:
            files.mkdir(result)

        # Check if value exists
        if os.path.isdir(result) is False:
            cache_message = (
                'cache_directory: "{}" '
                "in the configuration file(s) doesn't exist!"
            ).format(result)
            log.log2die_safe(1090, cache_message)

        # Return
        return result

    def daemon_log_file(self):
        """Get daemon_log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        result = "{}{}switchmap-poller.log".format(
            self.log_directory(), os.sep
        )

        # Return
        return result

    def hostnames(self):
        """Get hostnames.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = []
        candidates = self._config_poller.get("hostnames", [])

        # Get result
        if isinstance(candidates, list) is True:
            candidates = list(set(candidates))
            result = sorted(candidates)

        # Return
        return result

    def polling_interval(self):
        """Get polling_interval.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_poller.get("polling_interval", 86400)
        return result

    def snmp_auth(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            snmp_data: List of SNMP data dicts found in configuration file.

        """
        # Initialize key variables
        all_groups = self._config_poller.get("snmp_groups", [])
        template = {
            "snmp_version": 2,
            "snmp_secname": None,
            "snmp_community": None,
            "snmp_authprotocol": None,
            "snmp_authpassword": None,
            "snmp_privprotocol": None,
            "snmp_privpassword": None,
            "snmp_port": 161,
            "group_name": None,
            "enabled": True,
        }
        result = []

        # Read configuration's SNMP information. Return 'None' if none found
        if isinstance(all_groups, list) is True:
            if len(all_groups) < 1:
                return None
        else:
            return None

        # Start populating information
        for next_group in all_groups:
            # Next entry if this is not a dict
            if isinstance(next_group, dict) is False:
                continue

            # Assign good data
            new_dict = {}
            for key, _ in template.items():
                if key in next_group:
                    new_dict[key] = next_group[key]
                else:
                    new_dict[key] = template[key]

            # Convert relevant strings to integers
            new_dict["snmp_version"] = int(new_dict["snmp_version"])
            new_dict["snmp_port"] = int(new_dict["snmp_port"])

            # Append data to list
            result.append(new_dict)

        # Return
        return result
