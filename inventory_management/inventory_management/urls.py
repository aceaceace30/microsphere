from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('login/', login_view, name='login'),
    #TODO: overide the change password, change pass done, password reset, password reset done
    path('accounts/', include('django.contrib.auth.urls')),
    path('inventory/', include('inventory.urls')),
]

# django admin customization

# redirect page when clicking the 'view site' in django admin
admin.site.site_url = "/inventory/unit-list/"

admin.site.site_header = 'Microsphere | Inventory Management'
admin.site.site_title = 'Microsphere - Inventory Management'