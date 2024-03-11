"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import patterns as patterns
# from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from django.views.generic.base import TemplateView
from baton.autodiscover import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def trigger_error(request):
    division_by_zero = 1 / 0



urlpatterns = [
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path("users/", include("users.urls")),
    path("users/", include("django.contrib.auth.urls")),
    path("users/", include("allauth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("catalog/", include("suppliers.urls")),
    path("orders/", include("clients.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('sentry-debug/', trigger_error)

]

#
# urlpatterns = patterns('',
#     url(r'', include('social_auth.urls')),
# )