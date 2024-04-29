from django.urls import path
from ..views import *


urlpatterns = [
    path('signin', SigninView.as_view(), name='signin'),
    path('signup', SignupView.as_view(), name='signup'),
    path('signout', LogoutView.as_view(), name='signout'),
    path('verify/<str:email>/', VerifyEmailView.as_view(), name='verify'),

]
