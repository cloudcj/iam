from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import UpdateModelMixin

class PatchOnlyModelMixin(UpdateModelMixin):
  def update(self, request, *args, **kwargs):
    if request.method == "PUT":
      raise MethodNotAllowed("PUT", detail="PUT method not allowed. Use PATCH instead.")
    return super().update(request, *args, **kwargs)