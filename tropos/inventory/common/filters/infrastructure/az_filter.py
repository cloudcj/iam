from inventory.infrastructure.models import AvailabilityZone
from ..base_filter import BaseFilter

class AvailabilityZoneFilter(BaseFilter):
  class Meta:
    model = AvailabilityZone
    fields = []

AvailabilityZoneFilter.add_number_list_field("id")
AvailabilityZoneFilter.add_search_list_field("name")
# AvailabilityZoneFilter.add_exact_field(field_name="location")
# AvailabilityZoneFilter.add_exact_field(field_name="region__name")

AvailabilityZoneFilter.add_exact_field("location","region_name")

AvailabilityZoneFilter.search_fields = ["id", "name", "location", "region__name"]