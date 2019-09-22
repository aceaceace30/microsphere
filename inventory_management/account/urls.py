from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView
    #PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView,
)
from . import views

app_name = 'account'

urlpatterns = [

	path('dashboard/', views.dashboard, name="dashboard"),
	path('login/', LoginView.as_view(redirect_authenticated_user=True), name="login"),
	path('logout/', LogoutView.as_view(), name="logout"),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url='/accounts/password_change/done/'), name="password_change"),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name="password_change_done"),

]
