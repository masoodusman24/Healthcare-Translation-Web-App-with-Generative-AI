from django.urls import path
from translator import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/translate/', views.translate, name='translate'),
]
