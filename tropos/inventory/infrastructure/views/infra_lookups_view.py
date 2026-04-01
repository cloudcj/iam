# # views/lookups.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.db.models import Q
from django.core.cache import cache


from inventory.infrastructure.models import (
    Region,
    AvailabilityZone,
    Building,
    Floor,
    Room,
    Pod,
    Rack,
    RackPosition,
    PowerDeliveryUnit,
    PowerDeliveryUnitOutlet,
)

INFRA_LOOKUPS = {
    "regions": Region,
    "availability-zones": AvailabilityZone,
    "buildings": Building,
    "floors": Floor,
    "rooms": Room,
    "pods": Pod,
    "racks": Rack,
    "rack-positions": RackPosition,
    "pdus": PowerDeliveryUnit,
    "pdu-outlets": PowerDeliveryUnitOutlet,
}

def get_label(obj):
    if hasattr(obj, "name") and obj.name:
        return str(obj.name)

    if hasattr(obj, "number") and obj.number is not None:
        return str(obj.number)

    return str(obj)



class InfraLookupView(APIView):

    DEFAULT_LIMIT = 100
    CACHE_TTL = 300  # 5 minutes

    def get(self, request, model_name):
        model = INFRA_LOOKUPS.get(model_name)

        if not model:
            return Response(
                {"error": f"Invalid lookup '{model_name}'"},
                status=400,
            )

        # ----------------------------
        # Cache key
        # ----------------------------
        cache_key = self._cache_key(request, model_name)
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        # ----------------------------
        # Base queryset
        # ----------------------------
        qs = model.objects.all()

        # ----------------------------
        # FK filtering (?building=1)
        # ----------------------------
        for field in model._meta.fields:
            if isinstance(field, (ForeignKey, OneToOneField)):
                value = request.GET.get(field.name)
                if value:
                    qs = qs.filter(**{f"{field.name}_id": value})

        # ----------------------------
        # Limit only (no ordering assumptions)
        # ----------------------------
        qs = qs[: self.DEFAULT_LIMIT]

        # ----------------------------
        # Serialize
        # ----------------------------
        data = [
            {
                "value": obj.id,
                "label": get_label(obj),
            }
            for obj in qs
        ]

        # ----------------------------
        # Cache
        # ----------------------------
        cache.set(cache_key, data, self.CACHE_TTL)

        return Response(data)

    def _cache_key(self, request, model_name):
        params = "&".join(
            f"{k}={v}"
            for k, v in sorted(request.GET.items())
        )
        return f"infra_lookup:{model_name}:{params}"
    
# def get_label(obj):
#     """
#     Dynamically generate a human-readable label for any model instance.
#     Priority:
#     1. obj.name
#     2. obj.number
#     3. First related FK object with 'name'
#     4. str(obj)
#     """
#     if hasattr(obj, "name") and obj.name:
#         return obj.name

#     if hasattr(obj, "number"):
#         return str(obj.number)

#     for field in obj._meta.get_fields():
#         if isinstance(field, (ForeignKey, OneToOneField)):
#             related_obj = getattr(obj, field.name, None)
#             if related_obj and hasattr(related_obj, "name"):
#                 return related_obj.name

#     return str(obj)


# class InfraLookupView(APIView):
#     """
#     Generic lookup API for dropdowns.

#     Example usage:
#       /api/lookups/region/
#       /api/lookups/availabilityzone/?region=1
#       /api/lookups/building/?availability_zone=3&search=dc

#     Query params:
#       - search: text search (if model has 'name')
#       - limit: max number of results (default: 50)
#       - <fk_field>=<id>: dynamic FK filtering
#     """

#     permission_classes = [IsAuthenticated]
#     APP_LABEL = "infrastructure"
#     DEFAULT_LIMIT = 50
#     MAX_LIMIT = 200

#     def get(self, request, model_name):
#         # -------------------------------
#         # Resolve model (case-insensitive)
#         # -------------------------------
#         model = None
#         model_name_lower = model_name.lower()

#         for m in apps.get_app_config(self.APP_LABEL).get_models():
#             if m.__name__.lower() == model_name_lower:
#                 model = m
#                 break

#         if not model:
#             return Response(
#                 {"error": f"Invalid model name '{model_name}'"},
#                 status=400,
#             )

#         # -------------------------------
#         # Base queryset
#         # -------------------------------
#         qs = model.objects.all()

#         # -------------------------------
#         # FK-based dynamic filtering
#         # Example: ?region=1 → region_id=1
#         # -------------------------------
#         for field in model._meta.get_fields():
#             if isinstance(field, (ForeignKey, OneToOneField)):
#                 param_value = request.GET.get(field.name)
#                 if param_value:
#                     qs = qs.filter(**{f"{field.name}_id": param_value})

#         # -------------------------------
#         # Optional search (name only)
#         # -------------------------------
#         search_term = request.GET.get("search")
#         field_names = {f.name for f in model._meta.fields}

#         if search_term and "name" in field_names:
#             qs = qs.filter(name__icontains=search_term)

#         # -------------------------------
#         # Preload FK relations (N+1 safe)
#         # -------------------------------
#         fk_fields = [
#             f.name
#             for f in model._meta.get_fields()
#             if isinstance(f, (ForeignKey, OneToOneField))
#         ]

#         if fk_fields:
#             qs = qs.select_related(*fk_fields)

#         # -------------------------------
#         # Limit results
#         # -------------------------------
#         try:
#             limit = min(
#                 int(request.GET.get("limit", self.DEFAULT_LIMIT)),
#                 self.MAX_LIMIT,
#             )
#         except ValueError:
#             limit = self.DEFAULT_LIMIT

#         qs = qs[:limit]

#         # -------------------------------
#         # Build response
#         # -------------------------------
#         data = [
#             {
#                 "value": obj.id,
#                 "label": get_label(obj),
#             }
#             for obj in qs
#         ]

#         return Response(data)




# views/lookups.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.apps import apps
# from django.db.models.fields.related import ForeignKey, OneToOneField


# def get_label(obj):
#     """
#     Dynamically generate a human-readable label for any model instance.
#     - Uses 'name' if present
#     - Uses 'number' if present
#     - For ForeignKey fields, uses the related object's 'name' if available
#     - Fallback: str(obj)
#     """
#     # Check direct fields
#     if hasattr(obj, "name"):
#         return obj.name
#     if hasattr(obj, "number"):
#         return str(obj.number)

#     # Check for first foreign key that has a 'name' attribute
#     for field in obj._meta.get_fields():
#         if isinstance(field, (ForeignKey, OneToOneField)) and hasattr(getattr(obj, field.name, None), "name"):
#             related_obj = getattr(obj, field.name)
#             if related_obj:
#                 return related_obj.name

#     # Fallback
#     return str(obj)


# class InfraLookupView(APIView):
#     """
#     Generic lookup API for dropdowns.
#     Usage: /api/lookups/<model_name>/?search=term&limit=50
#     """
#     APP_LABEL = "infrastructure"

#     def get(self, request, model_name):
#         # Case-insensitive model lookup
#         model_name_lower = model_name.lower()
#         model = None
#         for m in apps.get_app_config(self.APP_LABEL).get_models():
#             if m.__name__.lower() == model_name_lower:
#                 model = m
#                 break

#         if not model:
#             return Response({"error": f"Invalid model name '{model_name}'"}, status=400)

#         # Base queryset
#         qs = model.objects.all()

#         # Optional search (only works if model has a 'name' field)
#         search_term = request.GET.get("search")
#         if search_term and "name" in [f.name for f in model._meta.fields]:
#             qs = qs.filter(name__icontains=search_term)

#         # Preload foreign keys to avoid N+1 queries
#         fk_fields = [f.name for f in model._meta.get_fields() if isinstance(f, (ForeignKey, OneToOneField))]
#         if fk_fields:
#             qs = qs.select_related(*fk_fields)

#         # Limit results (frontend dropdowns usually don't need thousands of rows)
#         limit = int(request.GET.get("limit", 50))
#         qs = qs[:limit]

#         # Build dropdown data
#         data = [{"value": obj.id, "label": get_label(obj)} for obj in qs]

#         return Response(data)















# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.apps import apps

# # Helper function for labels
# def get_label(obj):
#     """
#     Determine a human-readable label for any model instance.
#     """
#     if hasattr(obj, "name"):
#         label = obj.name
#     elif hasattr(obj, "number"):
#         label = str(obj.number)
#     elif hasattr(obj, "device") and obj.device:
#         label = getattr(obj.device, "name", str(obj.device_id))
#     else:
#         label = str(obj)
#     return label



# class InfraLookupView(APIView):
#     APP_LABEL = "infrastructure"

#     def get(self, request, model_name):
#         model_name_lower = model_name.lower()
#         model = None
#         for m in apps.get_app_config(self.APP_LABEL).get_models():
#             if m.__name__.lower() == model_name_lower:
#                 model = m
#                 break

#         if not model:
#             return Response({"error": f"Invalid model name '{model_name}'"}, status=400)

#         search_term = request.GET.get("search")
#         qs = model.objects.all()
#         if search_term and "name" in [f.name for f in model._meta.fields]:
#             qs = qs.filter(name__icontains=search_term)

#         data = [{"value": obj.id, "label": get_label(obj)} for obj in qs]
#         return Response(data)


# class InfraLookupView(APIView):
#     """
#     Generic lookup API for dropdowns.
#     Usage: /api/lookups/<model_name>/?search=term
#     """

#     APP_LABEL = "infrastructure"  # your Django app name

#     def get(self, request, model_name):
#         # Make model_name case-insensitive
#         model_name_lower = model_name.lower()
#         model = None
#         for m in apps.get_app_config(self.APP_LABEL).get_models():
#             if m.__name__.lower() == model_name_lower:
#                 model = m
#                 break

#         if not model:
#             return Response({"error": f"Invalid model name '{model_name}'"}, status=400)

#         # Filter by search query if provided
#         search_term = request.GET.get("search")
#         qs = model.objects.all()
#         if search_term and "name" in [f.name for f in model._meta.fields]:
#             qs = qs.filter(name__icontains=search_term)

#         # Serialize only id and name
#         data = [{"value": obj.id, "label": getattr(obj, "name")} for obj in qs]
#         return Response(data)
