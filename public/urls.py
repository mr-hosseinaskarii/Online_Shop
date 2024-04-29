from django.urls import path
from .views import ContactUsView, AboutUsView
# from .views import ComingSoonView

urlpatterns = [
    path('about', AboutUsView.as_view(), name='about'),
    path('contact', ContactUsView.as_view(), name='contact'),
    # path('', ComingSoonView.as_view(), name='coming_soon'),
]
