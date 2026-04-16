from django.urls import path
from core import views

urlpatterns = [
    path('user_login/',views.user_login, name='user_login'),
]

