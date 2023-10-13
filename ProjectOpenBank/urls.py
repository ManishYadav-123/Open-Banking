from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/api/v1/", include("coreapi.urls")),
    path("bank1/api/v1/", include("bank1.urls")),
    path("bank2/api/v1/", include("bank2.urls")),
    path("bank3/api/v1/", include("bank3.urls")),
    path("bank4/api/v1/", include("bank4.urls")),
    path("bank5/api/v1/", include("bank5.urls")),
    path("", include("coreapi.urls2")),
]
