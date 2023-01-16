from django.db import models

from django.db import models

class BitcoinPrice(models.Model):
    value = models.FloatField()
    btc_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
