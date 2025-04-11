"""
URL configuration for ai_agent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from web import settings
from web.views import IndexView, LivenessCheckView, QueryAiAgentView

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="CIT Datacenter Service AI AGENT",
        default_version='v1',
        description="AI Agent for interacting with the CIT Datacenter Microservice",
        license=openapi.License(name="DELL License"),
    ),
    public=True,
    permission_classes=(),
    authentication_classes=(),
    url=settings.SWAGGER_URL
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),  # Swagger UI
    path('health/liveness/', LivenessCheckView.as_view(), name='liveness_check'),
    path('api/v1/aiagent/query', QueryAiAgentView.as_view(), name='query_ai_agent'),
    
]
