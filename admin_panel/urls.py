from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_limits/', views.update_limits, name='update_limits'),
    path('get_logs/', views.get_logs, name='get_logs'),
]