"""Diop Machine model."""

from loguru import logger as log

from django.db import models

from .deliverygroup import DeliveryGroup


class Machine(models.Model):
    fqdn = models.CharField(
        "FQDN", max_length=64, primary_key=True, help_text="Fully Qualified Domain Name"
    )
    deliverygroup = models.ForeignKey(
        DeliveryGroup,
        on_delete=models.CASCADE,
        verbose_name="Delivery Group",
        help_text="Delivery Group the machine belongs to.",
    )
    state = models.CharField(
        "Machine State",
        max_length=16,
        help_text="Current machine status.",
    )
    powerstate = models.CharField("Power State", max_length=16)
    maintenance = models.BooleanField("Maintenance Mode", default=False)
    registration = models.CharField("Registration State", max_length=16)
    agent = models.CharField("Agent Version", max_length=32, null=True)
    active = models.BooleanField(
        "Active",
        default=True,
        help_text=(
            "Indicating if the machine is active or has been retired. Entries having "
            "this set to False will be ignored by update task completeness checks."
        ),
    )
    updated = models.BooleanField(
        "Updated",
        default=True,
        help_text=(
            "Flag tracking if the machine status is up-to-date. Has to be set to False "
            "by every function updating an entry and only re-set to True once the "
            "update has completed successfully."
        ),
    )
    req_maintenance = models.BooleanField(
        "Request Maintenance",
        default=False,
        help_text="Enter maintenance mode as soon as the machine is free.",
    )

    def __str__(self):
        return self.hostname

    @property
    def hostname(self):
        return self.fqdn.split(".")[0]

    @classmethod
    def get_or_new(cls, fqdn: str, dg_name: str, state: str = ""):
        """Get a machine object from the DB or create a new one.

        Queries the DB for an existing machine object, looking for the tuple (fqdn,
        deliverygroup), corresponding to parameters `fqdn` and `dg_name`. If no such
        entry exists, a new one will be created.

        Parameters
        ----------
        fqdn : str
            The machine's FQDN (pk of diop.models.Machine).
        dg_name : str
            The machine's delivery group (pk of diop.models.DeliveryGroup).
        state : str, optional
            An optional state to set for the machine entry. Useful when querying for
            a machine object using session information (which also contains the
            machine's state).

        Returns
        -------
        diop.models.Machine
        """
        fqdn = fqdn.lower()
        log.debug(f"🖥  Checking for machine [{fqdn}]...")

        if not state:
            state = "UNKNOWN"

        v_dg, _ = DeliveryGroup.get_or_new(dg_name)

        # query for the machine, passing in "state" to be used if a new record is
        # created (see below for *updating* the state on existing machines):
        v_machine, created = cls.objects.get_or_create(
            fqdn=fqdn,
            deliverygroup=v_dg,
            defaults={
                "state": state,
            },
        )

        if created:
            log.warning(f"🖥  Creating NEW machine: [{fqdn}] ✨")
        else:
            log.debug(f"🖥  Updating existing machine: [{fqdn}] 📝")

        # if the machine exists but "state" is differing we need to update (+ save)
        if v_machine.state != state:
            v_machine.state = state
            v_machine.save()

        return v_machine, created

    @classmethod
    def from_psy_session(cls, psy_session: dict):
        """Get a Machine object from a PSyTricks session dict.

        Parameters
        ----------
        psy_session : dict
            Session infos as returned by psytricks.ResTricksWrapper.get_sessions().

        Returns
        -------
        diop.models.Machine
            The DB record corresponding to the session machine.
        """
        fqdn = psy_session["DNSName"].lower()
        dg_name = psy_session["DesktopGroupName"]
        state = psy_session["MachineSummaryState"]

        v_machine, _ = cls.get_or_new(fqdn, dg_name, state)

        return v_machine
