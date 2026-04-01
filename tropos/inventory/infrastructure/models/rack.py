from django.db import models
from inventory.common.custom_models import TimestampedModel
from .pod import Pod
from inventory.enums.models import NetworkArea, NetworkAreaOrder

class Environment(models.TextChoices):
    TEST_LAB = 'TEST', 'Test Lab'
    PROD = 'PROD', 'Production'

class Rack(TimestampedModel):
  environment = models.CharField(max_length=10, choices=Environment.choices, null=True)
  pod = models.ForeignKey(Pod, on_delete=models.PROTECT)
  number = models.CharField(max_length=30)
  network_area = models.ForeignKey(NetworkArea, on_delete=models.PROTECT,null=True,blank=True,related_name='devices')
  network_area_order = models.ForeignKey(NetworkAreaOrder, on_delete=models.PROTECT, null=True,blank=True, related_name='devices')
  ru_count = models.PositiveSmallIntegerField(default=42)
  weight = models.PositiveSmallIntegerField()
  is_occupied = models.BooleanField(default=False, blank=True)

  def save(self, *args, **kwargs):
    is_new = self.pk is None  # check if this is a new instance
    super().save(*args, **kwargs)
    if is_new:
      from .rack import RackPosition
      from .power_delivery_unit import PowerDeliveryUnit, Type

      RackPosition.objects.bulk_create([
        RackPosition(rack=self, position_number=i+1) for i in range(42)
      ])
      PowerDeliveryUnit.objects.get_or_create(rack=self, position=Type.LEFT)
      PowerDeliveryUnit.objects.get_or_create(rack=self, position=Type.RIGHT)

  def update_occupancy(self):
    """
    Set is_occupied = True if *any* rack position is occupied
    """
    has_occupied = self.rack_positions.filter(is_occupied=True).exists()
    if self.is_occupied != has_occupied:
      self.is_occupied = has_occupied
      self.save(update_fields=["is_occupied"])

  class Meta:
     constraints = [
        models.UniqueConstraint(
           fields=['number', 'pod'],
           name='unique_rack_per_pod'
        )
     ]
  
  def __str__(self):
     return str(self.number)

class RackPosition(TimestampedModel): 
  rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="rack_positions")
  position_number = models.PositiveSmallIntegerField()
  is_occupied = models.BooleanField(default=False, blank=True)

  device = models.ForeignKey(
    'assets.Device',
    null=True, 
    blank=True, 
    on_delete=models.SET_NULL, 
    related_name="rack_positions"
  )

  def save(self, *args, **kwargs):
    # auto-set is_occupied depending on device presence
    self.is_occupied = self.device is not None
    super().save(*args, **kwargs)

    # after saving, update the parent rack
    self.rack.update_occupancy()
    
  class Meta:
    db_table = "infrastructure_rack_position"

    # Prevents Duplicates
    constraints = [
       models.UniqueConstraint(
        fields=['position_number', 'rack'], 
        name='unique_rack_position'
        ) 
    ]
    ordering = ['-position_number']  # top-down order (42 to 1)

