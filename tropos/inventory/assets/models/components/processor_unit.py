from django.db import models
from django.core.exceptions import ValidationError
from inventory.common.custom_models import TimestampedModel
from ..devices import Device
from inventory.enums.models import ProcessorBrand, ProcessorCodename, ProcessorTier, ProcessorModel



class ProcessorUnit(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="processor_units")
    processor_codename = models.ForeignKey(ProcessorCodename, on_delete=models.CASCADE, related_name="units", null=True)
    processor_tier = models.ForeignKey(ProcessorTier, on_delete=models.CASCADE, related_name="units", null=True)
    processor_model = models.ForeignKey(ProcessorModel, on_delete=models.CASCADE, related_name="units", null=True)

    def clean(self):
        # device = self.device

        # # Allow servers
        # if device.type == "server":
        #     return

        # # Allow appliances that have compute units
        # if device.type == "appliance":
        #     if device.appliance and device.appliance.has_components_units:
        #         return

        # raise ValidationError(
        #     "Only servers and appliances with compute units may have processor units."
        # )


       
        if self.device.type not in ["server", "appliance","analyzer"]:
            raise ValidationError("Only servers and appliances may have processor units.")
        
        if self.processor_model:
            # Model must match selected codename
            if self.processor_codename and self.processor_model.codename != self.processor_codename:
                raise ValidationError("Processor model does not match the selected codename.")

            # Model must match selected tier
            if self.processor_tier and self.processor_model.tier != self.processor_tier:
                raise ValidationError("Processor model does not match the selected tier.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.processor_model:
            return f"{self.processor_model.name} in {self.device}"
        return f"Processor Unit in {self.device}"



# class ProcessorUnit(TimestampedModel):
#     device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="processor_units")
#     processor_codename = models.ForeignKey(ProcessorCodename, on_delete=models.CASCADE, related_name="units", null=True)
#     processor_tier = models.ForeignKey(ProcessorTier, on_delete=models.CASCADE, related_name="units", null=True)
#     processor_model = models.ForeignKey(ProcessorModel,on_delete=models.CASCADE,related_name="units", null=True)

#     class Meta:
#         db_table = "assets_processor_unit"


    # def clean(self):
    #     if self.processor_model:
    #         if self.processor_model.codename_id != self.processor_codename_id:
    #             raise ValidationError("Model codename does not match selected codename.")

    #     if self.processor_model.tier_id != self.processor_tier_id:
    #         raise ValidationError("Model tier does not match selected tier.")

    #     if self.processor_model.brand_id != self.processor_codename.brand_id:
    #         raise ValidationError("Brand mismatch between model and codename/tier.")


    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return (
    #         f"{self.device.name} - "
    #         f"{self.processor_model.name} | "
    #         f"{self.processor_codename.name} | "
    #         f"{self.processor_tier.name}"
    #     )