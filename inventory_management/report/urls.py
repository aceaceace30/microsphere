from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
	path('count_report/', views.generate_count_report, name='generate_count_report'),
	path('certification_form/', views.CertificationFormView.as_view(), name='certification_form'),
	path('download_pm_attachments/', views.download_pm_attachments, name='download_pm_attachments'),
]