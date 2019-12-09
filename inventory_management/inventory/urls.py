from django.urls import path
from . import views
from .utils import UnitListJson, PmListJson, load_business_units, load_brand_choices, load_model_choices

app_name = 'inventory'

urlpatterns = [
    path('unit-list/', views.UnitListView.as_view(), name='unit-list'),
    path('unit-create/', views.UnitCreateView.as_view(), name='unit-create'),
    path('unit-view/<int:pk>/', views.UnitDetailView.as_view(), name='unit-view'),
    path('unit-edit/<int:pk>/', views.UnitUpdateView.as_view(), name='unit-edit'),
    path('unit-delete/<int:pk>/', views.unit_delete, name='unit-delete'),
    path('unit-view-json/<int:pk>/', views.unit_view_json, name='unit-view-json'),

    path('pm-list/', views.PmListView.as_view(), name='pm-list'),
    path('pm-create/', views.pm_create, name='pm-create'),
    path('pm-view/<int:pk>/', views.PmDetailView.as_view(), name='pm-view'),
    path('pm-edit/<int:pk>/', views.PmUpdateView.as_view(), name='pm-edit'),
    path('pm-delete/<int:pk>/', views.pm_delete, name='pm-delete'),
    #path('mark-as-done/<int:pk>/', views.mark_as_done, name='mark-as-done'), remove
    path('add-pm-remarks/<int:pk>/', views.add_pm_remarks, name='add-pm-remarks'),
    path('pm-mark-done/<int:pk>/', views.pm_mark_done, name='pm-mark-done'),
    path('pm-send-mail/<int:pk>/', views.pm_send_email, name='pm-send-mail'),
    path('save-service-report-no/<int:pk>/', views.save_service_report_no, name='save-service-report-no'),
    path('check-all-unit-done/<int:pk>/', views.check_all_unit_done, name='check-all-unit-done'),
    path('pm-upload-attachment/<int:pk>/', views.pm_upload_attachment, name='pm-upload-attachment'),

    path('unit-list/<int:pk>/', views.UnitPerBranch.as_view(), name='get_list_per_businessunit'),
    path('unit-history/<int:pk>/', views.unit_history, name='unit-history'),

    # ajax calls
    path('ajax/load-business-units/', load_business_units, name='load_business_units'),
    path('ajax/load-model-choices/', load_model_choices, name='load_model_choices'),
    path('ajax/load-brand-choices/', load_brand_choices, name='load_brand_choices'),

    # server side processing data table
    path('load-unit-datatable/', UnitListJson.as_view(), name='unit_list_json'),
    path('load-pm-datatable/', PmListJson.as_view(), name='pm_list_json'),

    # generate pdf
    path('generate-certification-form/<int:pk>/', views.GenerateCertificationForm.as_view(), name='generate_certification_form')
    
]