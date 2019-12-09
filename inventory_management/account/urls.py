from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from . import views

from django.conf import settings

app_name = 'account'

urlpatterns = [

	path('dashboard/', views.dashboard, name="dashboard"),
	path('login/', LoginView.as_view(redirect_authenticated_user=True, extra_context={'company_name':settings.COMPANY_NAME}), name="login"),
	path('logout/', LogoutView.as_view(), name="logout"),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url='/account/password_change/done/'), name="password_change"),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password_reset/', PasswordResetView.as_view(success_url='/account/password_reset/done/'), name="password_reset"),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url='/account/reset/done/'), name="password_reset_confirm"),
    path('reset/done/', PasswordResetCompleteView.as_view(), name="password_reset_complete")

]
