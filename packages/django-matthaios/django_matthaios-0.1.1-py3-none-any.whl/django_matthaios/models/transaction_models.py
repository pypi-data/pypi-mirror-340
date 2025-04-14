from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max

from .party_models import Party


class SalesDocument(models.Model):
    DOCUMENT_TYPES = [
        ("AR", "Accounts Receivable"),  # Party invoices CounterParty
        ("AP", "Accounts Payable"),  # CounterParty invoices Party
    ]

    party = models.ForeignKey(
        Party, related_name="sales_documents", on_delete=models.PROTECT
    )
    transaction = models.ForeignKey("Transaction", on_delete=models.CASCADE)
    counterparty = models.ForeignKey("CounterParty", on_delete=models.PROTECT)
    document_id = models.CharField(max_length=150)  # Alphanumeric
    document_type = models.CharField(
        max_length=2,
        choices=DOCUMENT_TYPES,
        default="AR",
    )
    issued_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=3, default="USD")  # ISO 4217 codes
    gross_amount = models.DecimalField(
        max_digits=28,
        decimal_places=2,
    )
    tax_amount = models.DecimalField(
        max_digits=28,
        decimal_places=2,
    )
    net_amount = models.DecimalField(
        max_digits=28,
        decimal_places=2,
    )
    document_type = models.CharField(
        max_length=2,
        choices=DOCUMENT_TYPES,
        default="AR",
    )
    amount_owed = models.DecimalField(
        max_digits=28,
        decimal_places=2,
    )


    

    class Meta:
        db_table_comment = "Sales documents linked to transactions (AR and AP)"

    def save(self, *args, **kwargs):
        if not self.pk and self.amount_owed == 0 and self.gross_amount > 0:
            self.amount_owed = self.gross_amount
        super().save(*args, **kwargs)

    def amount_paid(self):
        """Calculate the amount paid based on gross_amount and amount_owed."""
        return self.gross_amount - self.amount_owed

    def __str__(self):
        return f"{self.document_id} - {self.counterparty.name}"


class Journal(models.Model):
    JOURNAL_TYPES = [
        ("GL", "General Ledger"),
        ("AR", "Accounts Receivable"),
        ("AP", "Accounts Payable"),
        ("A", "Assorted"),
    ]

    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(
        max_length=2,
        choices=JOURNAL_TYPES,
        blank=True,
    )

    class Meta:
        db_table_comment = "A group of transactions that naturally belong together"


class Transaction(models.Model):
    journal = models.ForeignKey("Journal", on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50, unique=True, editable=False)
    transaction_type = models.CharField(
        max_length=10,
        choices=[("SALE", "Sale"), ("PURCH", "Purchase")],
    )
    documentation_date = models.DateField()  # New: Typically invoice date
    report_date = models.DateField()  # New: Date for reporting period
    voucher_type = models.CharField(max_length=10, blank=True)  # SAF-T: VoucherType
    voucher_description = models.CharField(
        max_length=255, blank=True
    )  # SAF-T: VoucherDescription
    description = models.CharField(max_length=255, blank=True)  # SAF-T: Description
    sequence = models.IntegerField(null=True, blank=True)

    def generate_transaction_id(self):
        year = self.documentation_date.year
        return f"{self.journal.party.party_number}-{self.transaction_type}-{year}-{self.sequence:08d}"

    def save(self, *args, **kwargs):
        if not self.sequence:
            max_sequence = (
                Transaction.objects.filter(
                    journal__party=self.journal.party,
                    transaction_type=self.transaction_type,
                    documentation_date__year=self.documentation_date.year,
                ).aggregate(Max("sequence"))["sequence__max"]
                or 0
            )
            if max_sequence >= 99999999:
                raise ValidationError(
                    "Maximum transactions (100M) per year per type reached."
                )
            self.sequence = max_sequence + 1
        self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_id


class Line(models.Model):
    transaction = models.ForeignKey("Transaction", on_delete=models.CASCADE)
    record_id = models.CharField(max_length=50, blank=True)  # SAF-T: RecordID
    account_id = models.CharField(max_length=50)  # SAF-T: AccountID
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    description = models.CharField(max_length=255, blank=True)  # SAF-T: Description

    funksjon_kapittel = models.CharField(
        max_length=4, null=True, blank=True
    )  # Funksjon gjelder bevilgningsregnskapet, kapittel gjelder balansen. Venstrejustert.
    art_sektor = models.CharField(
        max_length=3, null=True, blank=True
    )  #  Art gjelder bevilgningsregnskapet, sektor gjelder balansen.

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )  # Net amount posted = amount accounted

    gross_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )  # New: Total including tax

    deducted_tax_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )  # New: Tax deducted/reported
