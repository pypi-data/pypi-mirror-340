from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max

class PartySet(models.Model):
    name = models.CharField(max_length=100)
    parties = models.ManyToManyField("Party")

    class Meta:
        db_table_comment = (
            "Parties that naturally belong together, like a corporate group."
        )
        verbose_name = "Corporate Group"
        verbose_name_plural = "Corporate Groups"


class Party(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    party_number = models.CharField(max_length=6, unique=True)

    class Meta:
        db_table_comment = (
            "The starting point - the companies to which the transactions are stored."
        )
        verbose_name = "Party"
        verbose_name_plural = "Parties"

    def get_default_address(self, address_type):
        return self.addresses.filter(type=address_type, is_default=True).first()  # Updated

    def __str__(self):  # Added for admin readability
        return f"{self.name} ({self.party_number})"

class CounterParty(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table_comment = "Customers, suppliers etc."
        verbose_name = "Counterparty"
        verbose_name_plural = "Counterparties"

    def get_default_address(self, address_type):
        return self.addresses.filter(type=address_type, is_default=True).first()  # Updated

    def __str__(self):  # Added for admin readability
        return self.name

ADDRESS_TYPES = [
    ("SA", "StreetAddress"),
    ("PA", "PostalAddress"),
    ("BA", "BillingAddress"),
    ("ST", "ShipToAddress"),
    ("SF", "ShipFromAddress"),
]

class Address(models.Model):
    adr1 = models.CharField(max_length=500, null=True, blank=True, db_comment="StreetName")
    adr2 = models.CharField(max_length=500, null=True, blank=True, db_comment="AdditionalAddressDetail")
    postal_code = models.CharField(max_length=20, null=True, blank=True, db_comment="PostalCode")
    city = models.CharField(max_length=100, null=True, blank=True, db_comment="City")
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=2, null=True, blank=True)
    type = models.CharField(max_length=2, choices=ADDRESS_TYPES)
    party = models.ForeignKey(
        "Party",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="addresses"
    )
    counterparty = models.ForeignKey(
        "CounterParty",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="addresses"
    )
    is_default = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(party__isnull=False) | models.Q(counterparty__isnull=False),
                name="address_must_belong_to_party_or_counterparty"
            ),
            models.UniqueConstraint(
                fields=["party", "type"],
                condition=models.Q(is_default=True, counterparty__isnull=True),
                name="unique_default_address_per_type_party"
            ),
            models.UniqueConstraint(
                fields=["counterparty", "type"],
                condition=models.Q(is_default=True, party__isnull=True),
                name="unique_default_address_per_type_counterparty"
            )
        ]

    def save(self, *args, **kwargs):
        # Ensure address belongs to exactly one entity
        if (self.party and self.counterparty) or (not self.party and not self.counterparty):
            raise ValidationError("Address must belong to exactly one Party or CounterParty, not both or neither.")
        
        # Auto-set default for first address of type
        if self.party:
            existing = Address.objects.filter(party=self.party, type=self.type).exclude(id=self.id if self.id else None)
        else:  # self.counterparty
            existing = Address.objects.filter(counterparty=self.counterparty, type=self.type).exclude(id=self.id if self.id else None)
        
        if not existing.exists():
            self.is_default = True
        elif self.is_default:
            existing_default = existing.filter(is_default=True)
            if existing_default.exists():
                raise ValidationError(
                    f"{'Party' if self.party else 'CounterParty'} "
                    f"{self.party.party_number if self.party else self.counterparty.name} "
                    f"already has a default {self.type} address."
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.adr1 or 'Unnamed Address'} ({self.type})"