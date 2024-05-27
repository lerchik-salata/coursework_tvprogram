from datetime import timedelta
from django import forms
from .models import Channels, TVShows, ChannelShowTime
from django.contrib.auth.forms import AuthenticationForm


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channels
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'custom-control w-100',
                'placeholder': 'Enter the channel name',
                'autocomplete': 'off'
            }),
            'description': forms.Textarea(attrs={
                'class': 'custom-control w-100',
                'placeholder': 'Enter the channel description'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'custom-control w-100',
                'placeholder': 'Upload an image'
            }),
        }


class TVShowForm(forms.ModelForm):
    class Meta:
        model = TVShows
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'custom-control w-100',
                'placeholder': 'Enter the show name',
                'autocomplete': 'off'
            }),
            'description': forms.Textarea(attrs={
                'class': 'custom-control w-100',
                'placeholder': 'Enter the show description'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'custom-control w-100',
                'placeholder': 'Upload an image'
            }),
            'category': forms.Select(attrs={
                'class': 'custom-control w-100'
            }),
        }


class ChannelShowTimeForm(forms.ModelForm):
    class Meta:
        model = ChannelShowTime
        fields = '__all__'
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'custom-control w-100',
                'placeholder': 'Select start time'
            }),
            'channel': forms.Select(attrs={
                'class': 'custom-control w-100'
            }),
            'show': forms.Select(attrs={
                'class': 'custom-control w-100'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'custom-control w-100',
                'placeholder': 'Enter duration in minutes'
            }),
        }

    def clean(self):
        super().clean()

        start_time = self.cleaned_data.get('start_time', None)
        channel = self.cleaned_data.get('channel', None)
        duration = self.cleaned_data.get('duration')

        if duration < 5:
            raise forms.ValidationError('Duration must be at least 5 minutes.')

        if not start_time or not channel or not duration:
            raise forms.ValidationError('You must select a start time, channel, and duration.')

        end_time = start_time + timedelta(minutes=duration)

        overlapping_shows = ChannelShowTime.objects.filter(
            channel=channel,
            start_time__lt=end_time,
            start_time__gte=start_time - timedelta(minutes=duration)
        ).exclude(id=self.instance.id if self.instance else None)

        if overlapping_shows.exists():
            raise forms.ValidationError('Another show is already scheduled at this time. Please select another time.')

        return self.cleaned_data



class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'custom-control w-100',
            'placeholder': 'Enter your username'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'custom-control w-100',
            'placeholder': 'Enter your password'
        })
