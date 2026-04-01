from django.db import models
from django.core.exceptions import ValidationError

# -------------------------
# Brand
# -------------------------
class ProcessorBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        db_table = "enums_processor_brands"

    def __str__(self):
        return self.name

# -------------------------
# Codename
# -------------------------
class ProcessorCodename(models.Model):
    name = models.CharField(max_length=30)
    brand = models.ForeignKey(ProcessorBrand, on_delete=models.CASCADE, related_name="codenames")

    class Meta:
        db_table = "enums_processor_codenames"
        unique_together = ('name', 'brand')
        verbose_name = "Processor Codename"
        verbose_name_plural = "Processor Codenames"

    def __str__(self):
        return f"{self.name} ({self.brand.name})"

# -------------------------
# Tier
# -------------------------
class ProcessorTier(models.Model):
    name = models.CharField(max_length=30)
    brand = models.ForeignKey(ProcessorBrand, on_delete=models.CASCADE, related_name="tiers")

    class Meta:
        db_table = "enums_processor_tiers"
        unique_together = ("name", "brand")
        verbose_name = "Processor Tier"
        verbose_name_plural = "Processor Tiers"

    def __str__(self):
        return f"{self.name} ({self.brand.name})"

# =========================
# ProcessorModel
# =========================
class ProcessorModel(models.Model):
    name = models.CharField(max_length=100)
    codename = models.ForeignKey(ProcessorCodename, on_delete=models.CASCADE, related_name="models")
    tier = models.ForeignKey(ProcessorTier, on_delete=models.CASCADE, related_name="models")

    class Meta:
        unique_together = ('name', 'codename', 'tier')

    def clean(self):
        # Ensure the codename and tier exist
        if self.codename.brand_id != self.codename.brand_id:
            raise ValidationError("Processor model codename brand mismatch.")  # optional, usually redundant

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.codename.name} ({self.tier.name})"






# from django.db import models
# from django.core.exceptions import ValidationError

# # -------------------------
# # Brand
# # -------------------------
# class ProcessorBrand(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     class Meta:
#         verbose_name = "Brand"
#         verbose_name_plural = "Brands"
#         db_table = "enums_processor_brands"

#     def __str__(self):
#         return self.name

# # -------------------------
# # Codename
# # -------------------------
# class ProcessorCodename(models.Model):
#     name = models.CharField(max_length=30)
#     brand = models.ForeignKey(ProcessorBrand, on_delete=models.CASCADE, related_name="codenames")

#     class Meta:
#         db_table = "enums_processor_codenames"
#         unique_together = ('name', 'brand')  # ensures no duplicates per brand
#         verbose_name = "Processor Codename"
#         verbose_name_plural = "Processor Codenames"

#     def __str__(self):
#         return f"{self.name} ({self.brand.name})"
    
# # -------------------------
# # Tier
# # -------------------------
# class ProcessorTier(models.Model):
#     name = models.CharField(max_length=30)
#     brand = models.ForeignKey(ProcessorBrand, on_delete=models.CASCADE, related_name="tiers")

#     class Meta:
#         db_table = "enums_processor_tiers"
#         unique_together = ('name', 'brand')

#     def __str__(self):
#         return f"{self.name} ({self.brand.name})"    
    

# # =========================
# # ProcessorModel  (NEW)
# # =========================
# class ProcessorModel(models.Model):
#     name = models.CharField(max_length=100)

#     brand = models.ForeignKey(
#         ProcessorBrand,
#         on_delete=models.CASCADE,
#         related_name="models"
#     )

#     codename = models.ForeignKey(
#         ProcessorCodename,
#         on_delete=models.CASCADE,
#         related_name="models"
#     )

#     tier = models.ForeignKey(
#         ProcessorTier,
#         on_delete=models.CASCADE,
#         related_name="models"
#     )

#     class Meta:
#             unique_together = ('name', 'codename', 'tier', 'brand')

#     def clean(self):
#         # Ensure model's codename & tier belong to same brand as model.brand
#         if self.codename.brand_id != self.brand_id:
#             raise ValidationError("Processor model codename brand mismatch.")
#         if self.tier.brand_id != self.brand_id:
#             raise ValidationError("Processor model tier brand mismatch.")

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.name} - {self.codename.name} ({self.tier.name})"
