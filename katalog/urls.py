from django.urls import path
from . import views

app_name = 'katalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/manhwa/', views.api_manhwa_list, name='api_manhwa_list'),
    path('api/manhwa/<int:pk>/', views.api_manhwa_detail, name='api_manhwa_detail'),
    path('api/obiekty/', views.api_manhwa_list, name='api_obiekty'),
]
