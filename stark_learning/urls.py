from django.contrib import admin
from django.urls import path, re_path

from stark.service.version1 import site

print(site._registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'stark/', site.urls)
]
