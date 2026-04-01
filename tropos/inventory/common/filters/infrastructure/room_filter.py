from inventory.infrastructure.models import Room
from ..base_filter import BaseFilter

class RoomFilter(BaseFilter):
  class Meta:
    model = Room
    fields = []

# AvailabilityZoneFilter.add_number_list_field(field_name="id")
# AvailabilityZoneFilter.add_search_list_field(field_name="name")
# AvailabilityZoneFilter.add_exact_field(field_name="location")
# AvailabilityZoneFilter.add_exact_field(field_name="region__name")

RoomFilter.search_fields = ["id", "number", "location", "region__name"]