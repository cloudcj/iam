from django.db.models.query import QuerySet
from datetime import datetime, date
from django.db.models import Model
from inventory.logs.models.audit_log import AuditLog


def log_model_event(instance, action, user=None, changes=None):
  """
  Logs create, update, delete actions for any model instance.
  """
  token = getattr(user, '_token', None)
  user_id = token.get('sub') if token else None
  username = token.get('username') if token else getattr(user, 'username', 'system')
  department = token.get('department') if token else None

  AuditLog.objects.create(
    user_id=user_id,
    username=username,
    department=department,
    target=instance.__class__.__name__,
    target_id=str(instance.pk),
    action=action.lower(),
    detail=changes or {},
  )


def make_serializable(value):
  """
  Convert Django model fields to JSON-serializable values.
  """
  if isinstance(value, Model):
      return {"id": value.pk, "str": str(value)}

  if isinstance(value, (QuerySet, list, tuple, set)):
      return [make_serializable(v) for v in value]

  if isinstance(value, (datetime, date)):
      return value.isoformat()

  if isinstance(value, dict):
      return {k: make_serializable(v) for k, v in value.items()}

  return value
