from decimal import Decimal

from django.db import models


class DecimalField(models.DecimalField):
    def __init__(self, *args, json_decimal_places=None, **kw):
        super().__init__(*args, **kw)
        self.json_quantize = Decimal(10) ** -(
            json_decimal_places or self.decimal_places)

    def to_json(self, value):
        if value is None:
            return None
        return value.quantize(self.json_quantize)
