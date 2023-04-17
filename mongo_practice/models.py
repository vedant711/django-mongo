from djongo import models
from django.contrib.auth.models import AbstractUser

class Transactions(models.Model):
    transaction_type = models.CharField(max_length=10,null=False)
    amount = models.FloatField()
    balance = models.FloatField()
    user_id = models.CharField(max_length=100)


# class Entry(models.Model):
#     transactions = models.EmbeddedField(
#         model_container=Transactions,
#     )


class CustomUser(AbstractUser):
    balance = models.FloatField()
    pin = models.IntegerField()





