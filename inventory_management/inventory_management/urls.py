from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from account import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_login),
    path('account/', include('account.urls', namespace='account')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('report/', include('report.urls', namespace='report')),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# django admin customization
# redirect page when clicking the 'view site' in django admin
admin.site.site_url = '/account/dashboard/'

# overide header and title
admin.site.site_header = 'Microsphere | Inventory Management'
admin.site.site_title = 'Microsphere - Inventory Management'