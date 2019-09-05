from django.urls import path
from . import views

urlpatterns = [
    path('unit-list/', views.UnitListView.as_view(), name='unit-list'),
    path('unit-create/', views.unit_create, name='unit-create'),
    path('unit-view/<int:pk>/', views.UnitDetailView.as_view(), name='unit-view'),
    path('unit-edit/<int:pk>/', views.UnitUpdateView.as_view(), name='unit-edit'),
    #path('unit-edit/<int:pk>/', views.unit_edit, name='unit-edit'),
    path('unit-delete/<int:pk>/', views.unit_delete, name='unit-delete'),

    path('pm-list/', views.PmListView.as_view(), name='pm-list'),
    path('pm-create/', views.pm_create, name='pm-create'),
    path('pm-edit/<int:pk>/', views.pm_edit, name='pm-edit'),
    path('pm-delete/<int:pk>/', views.pm_delete, name='pm-delete'),

    path('<int:pk>/unit-list/', views.units_per_business_unit, name='get_list_per_businessunit'),
    path('<int:pk>/tag-pm-done-or-undone/', views.tag_pm_done_or_undone, name='pm-tag')
]