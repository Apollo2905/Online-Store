from django.db import models

class CancelRequest(models.Model):
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE)


