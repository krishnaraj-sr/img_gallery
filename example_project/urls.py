import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('photologue/', include('photologue.urls')),
                  path('ksrapp/', include('ksrapp.urls')),
                  path('', TemplateView.as_view(template_name="homepage.html"), name='homepage'),
                  path('__debug__/', include(debug_toolbar.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
