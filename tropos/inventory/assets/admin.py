from django.contrib import admin
from .models import (
    Device, 
    Appliance, 
    ApplianceChassis,
    Interface, 
    MemoryUnit, 
    PowerSupplyUnit, 
    ProcessorUnit, 
    StorageUnit, 
    Server, 
    Switch
)

# Register your models here.
admin.site.register(Device)
admin.site.register(Appliance)
admin.site.register(Interface)
admin.site.register(MemoryUnit)
admin.site.register(PowerSupplyUnit)
admin.site.register(ProcessorUnit)
admin.site.register(StorageUnit)
admin.site.register(Server)
admin.site.register(Switch)
admin.site.register(ApplianceChassis)
