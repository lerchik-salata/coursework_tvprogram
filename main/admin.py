from django.contrib import admin

from main.models import Channels, TVShows, ChannelShowTime

admin.site.register(Channels)
admin.site.register(TVShows)
admin.site.register(ChannelShowTime)