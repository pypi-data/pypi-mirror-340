from django.test import TestCase
from django.core.exceptions import ValidationError
from django_matthaios.models import PartySet, Party, CounterParty, Address

class PartyModelsTestCase(TestCase):
    def setUp(self):
        self.party1 = Party.objects.create(id=1, name="BigCorp", party_number="P001")
        self.party2 = Party.objects.create(id=2, name="SmallCo", party_number="P002")
        self.counterparty1 = CounterParty.objects.create(id=1, name="SupplierX")
        self.address1 = Address.objects.create(
            adr1="123 Main St", type="SA", party=self.party1
        )

    # PartySet Tests
    def test_partyset_creation(self):
        "Test creating a PartySet and adding Parties"
        partyset = PartySet.objects.create(name="CorpGroup")
        partyset.parties.add(self.party1, self.party2)
        self.assertEqual(partyset.name, "CorpGroup")
        self.assertEqual(partyset.parties.count(), 2)
        self.assertIn(self.party1, partyset.parties.all())

    # Party Tests
    def test_party_creation(self):
        "Test creating a Party with valid data"
        party = Party.objects.get(id=1)
        self.assertEqual(party.name, "BigCorp")
        self.assertEqual(party.party_number, "P001")
        self.assertEqual(str(party), "BigCorp (P001)")

    def test_party_unique_party_number(self):
        "Test that party_number must be unique"
        with self.assertRaises(Exception):
            Party.objects.create(id=3, name="DuplicateCo", party_number="P001")

    def test_party_get_default_address(self):
        "Test get_default_address method for Party"
        Address.objects.create(adr1="PO Box 456", type="PA", party=self.party1, is_default=True)
        default_sa = self.party1.get_default_address("SA")
        default_pa = self.party1.get_default_address("PA")
        self.assertEqual(default_sa.adr1, "123 Main St")
        self.assertEqual(default_pa.adr1, "PO Box 456")
        self.assertIsNone(self.party1.get_default_address("BA"))

    # CounterParty Tests
    def test_counterparty_creation(self):
        "Test creating a CounterParty with valid data"
        cp = CounterParty.objects.get(id=1)
        self.assertEqual(cp.name, "SupplierX")
        self.assertEqual(str(cp), "SupplierX")

    def test_counterparty_get_default_address(self):
        "Test get_default_address method for CounterParty"
        Address.objects.create(adr1="789 Elm St", type="SA", counterparty=self.counterparty1, is_default=True)
        default_sa = self.counterparty1.get_default_address("SA")
        self.assertEqual(default_sa.adr1, "789 Elm St")
        self.assertIsNone(self.counterparty1.get_default_address("PA"))

    # Address Tests
    def test_address_creation(self):
        "Test creating an Address with valid data"
        addr = Address.objects.get(adr1="123 Main St")
        self.assertEqual(addr.type, "SA")
        self.assertEqual(addr.party, self.party1)
        self.assertIsNone(addr.counterparty)
        self.assertTrue(addr.is_default)
        self.assertEqual(str(addr), "123 Main St (SA)")

    def test_address_auto_default(self):
        "Test that first Address of a type is auto-set as default"
        addr2 = Address.objects.create(adr1="456 Oak St", type="SA", party=self.party1)
        self.assertFalse(addr2.is_default)
        addr3 = Address.objects.create(adr1="PO Box 789", type="PA", party=self.party1)
        self.assertTrue(addr3.is_default)

    def test_address_default_validation(self):
        "Test that setting a second default Address raises ValidationError"
        with self.assertRaises(ValidationError) as cm:
            Address.objects.create(
                adr1="789 Pine St", type="SA", party=self.party1, is_default=True
            )
        self.assertIn("already has a default SA address", str(cm.exception))

    def test_address_exactly_one_owner(self):
        "Test that Address must belong to exactly one Party or CounterParty"
        with self.assertRaises(ValidationError) as cm:
            Address.objects.create(
                adr1="Invalid St", type="SA", party=self.party1, counterparty=self.counterparty1
            )
        self.assertIn("exactly one Party or CounterParty", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            Address.objects.create(adr1="NoOwner St", type="SA")
        self.assertIn("exactly one Party or CounterParty", str(cm.exception))

    def test_address_constraints(self):
        "Test database-level constraints for Address"
        Address.objects.create(adr1="New SA", type="SA", party=self.party2, is_default=True)
        with self.assertRaises(Exception):
            Address.objects.create(adr1="Another SA", type="SA", party=self.party2, is_default=True)

        Address.objects.create(adr1="CP SA", type="SA", counterparty=self.counterparty1, is_default=True)
        with self.assertRaises(Exception):
            Address.objects.create(adr1="CP SA 2", type="SA", counterparty=self.counterparty1, is_default=True)

    def test_address_null_fields(self):
        "Test that nullable fields in Address can be blank"
        addr = Address.objects.create(type="SA", party=self.party2)
        self.assertIsNone(addr.adr1)
        self.assertIsNone(addr.adr2)
        self.assertIsNone(addr.postal_code)
        self.assertIsNone(addr.city)
        self.assertIsNone(addr.region)
        self.assertIsNone(addr.country)