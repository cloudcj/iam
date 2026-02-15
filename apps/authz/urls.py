from django.urls import path
from .views.authorize import AuthorizeView
from .views.batch_authorize import BatchAuthorizeView

urlpatterns = [
    path("authorize/", AuthorizeView.as_view(), name="iam-authorize"),
    path("authorize/batch/", BatchAuthorizeView.as_view())
]
