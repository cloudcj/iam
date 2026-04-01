from django.db import models

# TextChoices for storage type
class StorageType(models.TextChoices):
    HDD = "HDD", "HDD"
    SSD = "SSD", "SSD"

# TextChoices for capacity unit
class CapacityUnit(models.TextChoices):
    TB = "TB", "TB"
    GB = "GB", "GB"

# Lookup table for storage interface
class StorageInterface(models.Model):
    name = models.CharField(max_length=50)  # e.g., SATA, NVMe

    class Meta:
        db_table = "enums_storage_interface"

    def __str__(self):
        return self.name

# Lookup table for storage form factor
class StorageFormFactor(models.Model):
    name = models.CharField(max_length=50)  # e.g., 2.5", 3.5", M.2 2280

    class Meta:
        db_table = "enums_storage_formfactor"

    def __str__(self):
        return self.name
