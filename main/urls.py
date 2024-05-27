from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'main'

urlpatterns = [
    path('', ChannelShowTimeListView.as_view(), name='tvshows'),
    path('tvshows/<int:pk>', TVShowDetailView.as_view(), name='tvshow_detail'),
    path('channel/<int:pk>/<str:start_date>/', ChannelDetailView.as_view(), name='channel_detail_with_date'),
    path('channel/<int:pk>/', ChannelDetailView.as_view(), name='channel_detail_without_date'),

    path('channels/new/', ChannelCreateView.as_view(), name='channel_create'),
    path('channels/<int:pk>/edit/', ChannelUpdateView.as_view(), name='channel_update'),
    path('channels/<int:pk>/delete/', ChannelDeleteView.as_view(), name='channel_delete'),

    path('tvshows/new/', TVShowCreateView.as_view(), name='tvshow_create'),
    path('tvshows/<int:pk>/edit/', TVShowUpdateView.as_view(), name='tvshow_update'),
    path('tvshow/<int:pk>/delete/', TVShowDetailView.as_view(), name='tvshow_delete'),

    path('showtime/new/', ChannelShowTimeCreateView.as_view(), name='showtime_create'),
    path('showtime/<int:pk>/edit/', ChannelShowTimeUpdateView.as_view(), name='showtime_update'),
    path('showtime/<int:pk>/delete/', ChannelShowTimeDeleteView.as_view(), name='showtime_delete'),

    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
]

