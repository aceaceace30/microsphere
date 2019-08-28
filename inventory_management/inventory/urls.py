from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.UnitListView.as_view(), name='unit-list'),
    path('create/', views.unit_create, name='unit-create'),
    path('edit/<int:pk>/', views.unit_edit, name='unit-edit'),
    path('delete/<int:pk>/', views.unit_delete, name='unit-delete'),
]