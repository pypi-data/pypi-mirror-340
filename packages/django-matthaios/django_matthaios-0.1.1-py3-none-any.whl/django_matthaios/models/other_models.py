from django.db import models


class Documents(models.Model):
    pass

    class Meta:
        db_table_comment = (
            "Documents may be connected to transactions and sales documents."
        )
