from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include(('store.urls', 'store'), namespace='store')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('staff/', include(('staff.urls', 'staff'), namespace='staff')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
