from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ecommerce import views

urlpatterns = [
    path("permissions/", views.PermissionList.as_view()),
    path("permissions/<int:pk>/", views.PermissionDetail.as_view()),
    path("roles/", views.RoleList.as_view()),
    path("roles/<int:pk>/", views.RoleDetail.as_view()),
    path("users/", views.PersonList.as_view()),
    path("users/<int:pk>/", views.PersonDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
