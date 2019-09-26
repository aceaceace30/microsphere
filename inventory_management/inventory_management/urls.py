from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_login),
    path('accounts/', include('account.urls', namespace='accounts')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
]

# django admin customization

# redirect page when clicking the 'view site' in django admin
admin.site.site_url = '/accounts/dashboard/'

# overide header and title
admin.site.site_header = 'Microsphere | Inventory Management'
admin.site.site_title = 'Microsphere - Inventory Management'