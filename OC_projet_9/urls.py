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
    path('', myauth.views.LoginView.as_view(), name='login'),
    path('logout/', myauth.views.LogoutView.as_view(), name='logout'),
    path('signup/', myauth.views.SignupView.as_view(), name='signup'),
    path('home/', litrevu.views.HomeView.as_view(), name='home'),
    path('ticket/create/', litrevu.views.TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/update/<int:ticket_id>/', litrevu.views.TicketUpdateView.as_view(), name='ticket_update'),
    path('ticket/delete/<int:ticket_id>/', litrevu.views.TicketDeleteView.as_view(), name='ticket_delete'),
    path('review/create/<int:ticket_id>/', litrevu.views.ReviewCreateView.as_view(), name='review_create'),
    path('review/update/<int:review_id>/', litrevu.views.ReviewUpdateView.as_view(), name='review_update'),
    path('review/delete/<int:review_id>/', litrevu.views.ReviewDeleteView.as_view(), name='review_delete'),
    path('ticket_review/create/', litrevu.views.TicketReviewCreateView.as_view(), name='ticket_review_create'),
    path('subscription/follow/', litrevu.views.FollowView.as_view(), name='follow'),
    path('subscription/follow/delete/<int:relation_id>/',
         litrevu.views.FollowDeleteView.as_view(), name='follow_delete'),
    path('subscription/block/', litrevu.views.BlockView.as_view(), name='block'),
    path('subscription/block/delete/<int:relation_id>/',
         litrevu.views.BlockDeleteView.as_view(), name='block_delete'),
    path('posts/', litrevu.views.PostsView.as_view(), name='posts'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
