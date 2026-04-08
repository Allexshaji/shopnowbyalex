from django.urls import path
from core import views

urlpatterns = [
    path('login/',views.user_login, name='user_login'),
]

