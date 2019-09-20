from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #TODO: overide the change password, change pass done, password reset, password reset done
    path('accounts/', include('account.urls', namespace='accounts')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
]

# django admin customization

# redirect page when clicking the 'view site' in django admin
admin.site.site_url = "/inventory/unit-list/"

# overide header and title
admin.site.site_header = 'Microsphere | Inventory Management'
admin.site.site_title = 'Microsphere - Inventory Management'