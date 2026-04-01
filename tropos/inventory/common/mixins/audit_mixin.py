from django.forms.models import model_to_dict
from ..helpers import log_model_event, make_serializable

class AuditLogMixin:
  """
  DRF view mixin to automatically log create, update, delete actions.
  """

  def perform_create(self, serializer):
    instance = serializer.save()
    new_values = {
        k: make_serializable(v) for k, v in serializer.validated_data.items()
    }

    log_model_event(
        instance,
        action="CREATE",
        changes=new_values,
        user=self.request.user,
    )

  def perform_update(self, serializer):
    # Old state before save
    instance = serializer.instance
    old_values = {
        k: make_serializable(v) for k, v in model_to_dict(instance).items()
    }

    # Save new state
    instance = serializer.save()
    new_values = {
        k: make_serializable(v) for k, v in model_to_dict(instance).items()
    }

    # Compute diffs
    changes = {
        field: {"old": old_values.get(field), "new": new_values.get(field)}
        for field in new_values
        if old_values.get(field) != new_values.get(field)
    }

    log_model_event(
        instance,
        action="UPDATE",
        changes=changes,
        user=self.request.user
    )

  def perform_destroy(self, instance):
    old_values = {
        k: make_serializable(v) for k, v in model_to_dict(instance).items()
    }

    log_model_event(
        instance,
        action="DELETE",
        changes=old_values,
        user=self.request.user
    )
    instance.delete()
