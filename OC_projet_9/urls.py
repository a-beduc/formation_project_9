"""
URL configuration for OC_projet_9 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import myauth.views
import litrevu.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', myauth.views.login_page, name='login'),
    path('logout/', myauth.views.logout_user, name='logout'),
    path('home/', litrevu.views.home, name='home'),
    path('signup/', myauth.views.signup_page, name='signup'),
    path('ticket/upload/', litrevu.views.ticket_upload, name='ticket_upload'),
    path('ticket/<int:ticket_id>/', litrevu.views.ticket_edit, name='ticket_edit'),
    path('review/upload/<int:ticket_id>/', litrevu.views.review_upload, name='review_upload'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
