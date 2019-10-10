from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('unit-list/', views.UnitListView.as_view(), name='unit-list'),
    path('unit-create/', views.unit_create, name='unit-create'),
    path('unit-view/<int:pk>/', views.unit_details, name='unit-view'),
    path('unit-edit/<int:pk>/', views.UnitUpdateView.as_view(), name='unit-edit'),
    #path('unit-edit/<int:pk>/', views.unit_edit, name='unit-edit'),
    path('unit-delete/<int:pk>/', views.unit_delete, name='unit-delete'),

    path('pm-list/', views.PmListView.as_view(), name='pm-list'),
    path('pm-create/', views.pm_create, name='pm-create'),
    path('pm-view/<int:pk>/', views.PmDetailView.as_view(), name='pm-view'),
    path('pm-edit/<int:pk>/', views.PmUpdateView.as_view(), name='pm-edit'),
    path('pm-delete/<int:pk>/', views.pm_delete, name='pm-delete'),
    path('mark-as-done/<int:pk>/', views.mark_as_done, name='mark-as-done'),
    path('add-pm-remarks/<int:pk>/', views.add_pm_remarks, name='add-pm-remarks'),

    path('unit-list/<int:pk>/', views.UnitPerBranch.as_view(), name='get_list_per_businessunit'),
    path('unit-history/<int:pk>/', views.unit_history, name='unit-history'),

    path('reports/', views.report_main, name='report-main'),

    # ajax calls
    path('ajax/load-business-units/', views.load_business_units, name='load_business_units')
    
]