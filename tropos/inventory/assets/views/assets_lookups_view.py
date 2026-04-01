# views/lookups.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps

class AssetsLookupView(APIView):
    """
    Generic lookup API for dropdowns.
    Usage: /api/lookups/<model_name>/?search=term
    """

    APP_LABEL = "assets"  # your Django app name

    def get(self, request, model_name):
        # Make model_name case-insensitive
        model_name_lower = model_name.lower()
        model = None
        for m in apps.get_app_config(self.APP_LABEL).get_models():
            if m.__name__.lower() == model_name_lower:
                model = m
                break

        if not model:
            return Response({"error": f"Invalid model name '{model_name}'"}, status=400)

        # Filter by search query if provided
        search_term = request.GET.get("search")
        qs = model.objects.all()
        if search_term and "name" in [f.name for f in model._meta.fields]:
            qs = qs.filter(name__icontains=search_term)

        # Serialize only id and name
        data = [{"value": obj.device.id, "label": obj.device.name} for obj in qs]
        return Response(data)
