"""labExperiment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from labExperiment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # high level paths that should not return anything
    path('experiments/<str:experiment_name>/<str:experiment_instance>/', views.experiment),
    path('experiments', views.global_index),
    path('', views.global_index),

]
