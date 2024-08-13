from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ecommerce import views

router = DefaultRouter()
router.register(r"roles", views.RoleDetail, basename="role")
router.register(r"persons", views.PersonDetail, basename="person")

urlpatterns = [
    path("permissions/", views.PermissionList.as_view(), name="permission-list"),
    path(
        "permissions/<int:pk>/",
        views.PermissionDetail.as_view(),
        name="permission-detail",
    ),
    path("", include(router.urls)),
]
