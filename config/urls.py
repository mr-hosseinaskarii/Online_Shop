from django.contrib import admin
from django.urls import path, include
from public.views import Error404View, Error500View


handler404 = Error404View.as_view()
handler500 = Error500View.as_view()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("public.urls")),
    path("", include("apps.shop.urls")),
    path("auth/", include("apps.accounts.urls")),
    path("accounts/", include("allauth.urls")),
]
