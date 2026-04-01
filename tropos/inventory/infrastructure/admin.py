from django.contrib import admin
from .models import Region, AvailabilityZone,  Building, Floor, Room, Pod, Rack, RackPosition, PowerDeliveryUnit, \
    PowerDeliveryUnitOutlet

# Register your models here.
admin.site.register(Region)
admin.site.register(AvailabilityZone)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Pod)
admin.site.register(Rack)
admin.site.register(RackPosition)
admin.site.register(PowerDeliveryUnit)
admin.site.register(PowerDeliveryUnitOutlet)