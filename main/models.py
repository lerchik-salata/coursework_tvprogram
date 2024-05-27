from datetime import timedelta
from django.db import models
from django.utils.timezone import now


class Channels(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='channel_images')

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"

    def __str__(self):
        return self.name


class TVShows(models.Model):
    CATEGORY_CHOICES = [
        ('DR', 'Drama'),
        ('CM', 'Comedy'),
        ('AC', 'Action'),
        ('SF', 'Science Fiction'),
        ('RM', 'Romance'),
        ('TH', 'Thriller'),
        ('AD', 'Adventure'),
    ]

    CATEGORY_DICT = dict(CATEGORY_CHOICES)

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='tvshow_images')
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "TVShow"
        verbose_name_plural = "TVShows"

    def __str__(self):
        return self.name

    def get_category_full(self):
        return self.CATEGORY_DICT.get(self.category)



class ChannelShowTime(models.Model):
    channel = models.ForeignKey(Channels, on_delete=models.CASCADE)
    show = models.ForeignKey(TVShows, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=now, null=True, blank=True)
    duration = models.FloatField(default=0, null=True, blank=True)

    @property
    def get_end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    def __str__(self):
        return f"{self.channel} - {self.show} - {self.start_time}"