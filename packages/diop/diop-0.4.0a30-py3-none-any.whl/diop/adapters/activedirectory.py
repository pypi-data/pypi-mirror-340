"""Adapter module to pull data from an ActiveDirectory."""

import ldap

from django.conf import settings

from box import Box
from loguru import logger as log

from ..models import User


LDAP_SERVER = settings.AUTH_LDAP_SERVER_URI
BIND_DN = settings.AUTH_LDAP_BIND_DN
BIND_PW = settings.AUTH_LDAP_BIND_PASSWORD
BASE_DN = settings.AUTH_LDAP_BASE_DN

DIOP_USER_AD_GROUP = settings.DIOP_USER_AD_GROUP

AD_GROUP_FILTER = "(&(objectClass=GROUP)(cn={group_name}))"
AD_USER_FILTER_PERSON = "(&(objectClass=USER)(objectCategory=person))"


class ActiveDirectory:
    """A connection wrapper to fetch information from an ActiveDirectory (AD).

    Attributes
    ----------
    conn : LDAPObject
        The LDAP connection object.
    ad_group : str
        The name of the AD group being used by all group-related operations.
    """

    def __init__(
        self,
        bind_dn=BIND_DN,
        bind_pw=BIND_PW,
        ldap_uri=LDAP_SERVER,
        ad_group=DIOP_USER_AD_GROUP,
    ):
        """ActiveDirectory constructor.

        Parameters
        ----------
        bind_dn : str, optional
            The bind DN ("bind user name"), by default BIND_DN.
        bind_pw : str, optional
            The bind credentials ("bind user password"), by default BIND_PW-
        ldap_uri : str, optional
            The address of the LDAP / AD server, by default LDAP_SERVER.
        ad_group : str, optional
            The name of the group to get the members for, e.g. `XY-VDI-Users`.

        Raises
        ------
        Exception
            Any exception raised during the "bind" action will be re-raised.
        """
        self.ad_group = ad_group
        self._group_members = []
        self._group_members_usernames = []
        self.user_details = {}

        log.debug(f"Trying to connect to [{ldap_uri}]...")
        conn = ldap.initialize(ldap_uri)
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)
        try:
            conn.simple_bind_s(who=bind_dn, cred=bind_pw)
        except Exception as err:
            log.error(f"LDAP bind failed: {err}")
            raise err

        self.conn = conn
        log.debug(f"Successfully connected to [{ldap_uri}].")

    @property
    def group_members(self) -> list:
        """A list of user-DN's being member of the configured AD group."""
        if not self._group_members:
            self._group_members = self.get_group_members(self.ad_group)

        return self._group_members

    @property
    def group_members_usernames(self) -> list:
        """A list of usernames being member of the configured AD group."""
        if not self._group_members_usernames:
            self._group_members_usernames = self.get_group_members_usernames(
                self.group_members
            )

        return self._group_members_usernames

    def get_group_members(self, group):
        """Query the AD to retrieve a list of user-DN's being member of a group.

        If any of the DN's in the list looks like a group-DN instead of a
        user-DN (contains the sequence "Group") a recursive lookup is attempted
        by using the value of the DN's first element as the group name. In case
        the recursive lookup fails, that DN is omitted and a warning message is
        issued to the log.

        Parameters
        ----------
        group : str
            The name of the group to get the members for, e.g. `XY-VDI-Users`.

        Returns
        -------
        list(str)
            A list of user DN's.
        """
        filter = AD_GROUP_FILTER.replace("{group_name}", group)
        result = self.conn.search_s(BASE_DN, ldap.SCOPE_SUBTREE, filter)
        raw_members = result[0][1]["member"]

        members = []
        for member in raw_members:
            try:
                # sanitize by force-decoding (assuming it is UTF-8):
                member = member.decode("utf-8")
            except:
                pass

            if "Group" not in member:
                members.append(member)
                continue

            log.debug(f"Potential group: {member}")
            try:
                group_name = member.split(",")[0].split("=")[1]
                members += self.get_group_members(group_name)
            except Exception as err:
                log.warning(f"Unable to resolve [{member}]: {err}")

        log.debug(f"Got {len(members)} members for group [{group}].")
        return members

    def get_group_members_usernames(self, group_members_dn) -> list:
        """Fetch usernames for the given list of group member DN's.

        Parameters
        ----------
        group_members_dn : list(str)
            The group members DN's to fetch the usernames for.

        Returns
        -------
        list
        """
        usernames = []
        for user_dn in group_members_dn:
            details = self.user_details_from_dn(user_dn)
            if details:
                usernames.append(details.username)
        log.debug(f"Got {len(usernames)} usernames.")
        return usernames

    def user_details_from_dn(self, user_dn) -> Box:
        """Fetch display name, email and department for a user DN.

        Parameters
        ----------
        user_dn : str or str-like
            The user-DN to fetch details for.

        Returns
        -------
        Box
            A Box with the attributes listed below, or `None` in case the lookup
            failed:

            - `username` : str
            - `display_name` : str
            - `email` : str
            - `department` : str
            - `enabled` : bool
        """
        try:
            # sanitize by force-decoding (assuming it is UTF-8):
            user_dn = user_dn.decode("utf-8")
        except:
            pass

        log.debug(f"Getting details for [{user_dn}]...")
        result = self.conn.search_s(user_dn, ldap.SCOPE_BASE, AD_USER_FILTER_PERSON)
        if len(result) < 1:
            log.warning(f"No results for user DN [{user_dn}]!")
            return None

        if len(result) > 1:
            log.error(f"Huh?! Got multiple results for user DN [{user_dn}]!")
            return None

        details = result[0][1]
        display_name = details["displayName"][0].decode("utf-8")
        email = details["mail"][0].decode("utf-8")
        username = details["sAMAccountName"][0].decode("utf-8")
        user_account_control = details["userAccountControl"][0].decode("utf-8")
        enabled = True if not int(user_account_control) & 0x002 else False
        try:
            department = details["department"][0].decode("utf-8")
        except:  # ruff: noqa: E722 (bare-except)
            department = ""

        details = Box(
            {
                "username": username,
                "display_name": display_name,
                "email": email,
                "department": department,
                "enabled": enabled,
            }
        )
        # store in the object's dict `user_details` using `username` as the key:
        self.user_details[username] = details

        return details
