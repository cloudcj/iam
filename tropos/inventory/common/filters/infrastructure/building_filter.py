from inventory.infrastructure.models import Building
from ..base_filter import BaseFilter

class BuildingFilter(BaseFilter):
  class Meta:
    model = Building
    fields = []

# BuildingFilter.add_number_list_field(field_name="id")
# BuildingFilter.add_search_list_field(field_name="name")
BuildingFilter.add_exact_field("location")
BuildingFilter.add_number_field(field_name="availability_zone", param_name="availability_zone_id")

BuildingFilter.search_fields = ["id", "name", "availability_zone__location", "availability_zone__name"]