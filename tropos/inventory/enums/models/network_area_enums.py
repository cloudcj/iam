from django.db import models

class NetworkArea(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = "enums_network_area"

    def __str__(self):
        return self.name

class NetworkAreaOrder(models.Model):
    name = models.CharField(max_length=40, unique=True)
    area = models.ForeignKey(NetworkArea, on_delete=models.CASCADE, related_name="orders")

    class Meta:
            db_table = "enums_network_area_order"

    def __str__(self):
        return self.name