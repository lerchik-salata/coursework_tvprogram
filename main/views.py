from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from coursework.settings import TIME_ZONE
from main.models import Channels, TVShows, ChannelShowTime
from django.urls import reverse_lazy, reverse
from .forms import ChannelForm, TVShowForm, ChannelShowTimeForm
from django.utils.timezone import now
import pytz
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class ChannelShowTimeListView(ListView):
    model = ChannelShowTime
    template_name = 'tv_program.html'
    context_object_name = 'channel_showtimes'
    current_timezone = pytz.timezone(TIME_ZONE)
    current_time = now().astimezone(current_timezone)

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.GET.get('start_date')
        if not start_date:
            start_date = self.current_time.date()

        sort = self.request.GET.get('sort', 'channels')
        queryset = queryset.filter(start_time__date=start_date)

        if sort == 'channels':
            queryset = queryset.order_by('channel__name', 'start_time')
        elif sort == 'time':
            queryset = queryset.order_by('start_time')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort = self.request.GET.get('sort', 'channels')
        start_date = self.request.GET.get('start_date')
        if not start_date:
            start_date = self.current_time.date()

        context['sort'] = sort
        context['start_date'] = start_date

        channel_data = {}
        for channel_showtime in context['channel_showtimes']:
            channel = channel_showtime.channel
            show = channel_showtime.show
            start_time = channel_showtime.start_time
            end_time = channel_showtime.get_end_time

            if channel not in channel_data:
                channel_data[channel] = []

            channel_data[channel].append({
                'show': show,
                'show_category': show.category,
                'start_time': start_time,
                'end_time': end_time,
                'show_id': show.id,
                'channel_id': channel.id,
            })

        context['channel_data'] = channel_data

        for channel, shows in channel_data.items():
            context['channel_detail_url'] = reverse('main:channel_detail_with_date', args=[channel.id, start_date])

        return context

    def get(self, request, *args, **kwargs):
        if 'start_date' not in request.GET:
            return redirect(f"{request.path}?start_date={self.current_time.date()}&sort={request.GET.get('sort', 'channels')}")
        return super().get(request, *args, **kwargs)


class TVShowDetailView(DetailView):
    model = TVShows
    template_name = 'tvshow_detail.html'
    context_object_name = 'show'


class ChannelDetailView(DetailView):
    model = Channels
    template_name = 'channel_detail.html'
    context_object_name = 'channel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        channel = self.get_object()
        current_timezone = pytz.timezone(TIME_ZONE)
        current_time = timezone.now().astimezone(current_timezone)
        start_date_str = self.kwargs.get('start_date')

        if start_date_str:
            start_date = timezone.datetime.fromisoformat(start_date_str).astimezone(current_timezone).date()
        else:
            start_date = current_time.date()

        current_time = timezone.datetime.combine(start_date, timezone.datetime.min.time()).astimezone(current_timezone)
        end_date = current_time + timedelta(days=7)

        channel_shows_times = channel.channelshowtime_set.select_related('show').filter(
            start_time__gte=current_time,
            start_time__lt=end_date
        ).order_by('start_time')

        shows_by_day = {}
        for showtime in channel_shows_times:
            day = showtime.start_time.astimezone(current_timezone).date()
            if day not in shows_by_day:
                shows_by_day[day] = []
            shows_by_day[day].append(showtime)

        context['shows_by_day'] = shows_by_day
        return context


class ChannelCreateView(LoginRequiredMixin, CreateView):
    model = Channels
    form_class = ChannelForm
    template_name = 'channel_form.html'
    success_url = reverse_lazy('main:account')
    login_url = 'main:login'


class ChannelUpdateView(LoginRequiredMixin, UpdateView):
    model = Channels
    form_class = ChannelForm
    template_name = 'channel_form.html'
    success_url = reverse_lazy('main:account')
    login_url = 'main:login'


class ChannelDeleteView(DeleteView):
    model = Channels
    success_url = reverse_lazy('main:account')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class TVShowCreateView(LoginRequiredMixin, CreateView):
    model = TVShows
    form_class = TVShowForm
    template_name = 'tvshow_form.html'
    success_url = reverse_lazy('main:account')
    login_url = 'main:login'


class TVShowUpdateView(LoginRequiredMixin, UpdateView):
    model = TVShows
    form_class = TVShowForm
    template_name = 'tvshow_form.html'
    success_url = reverse_lazy('main:account')
    login_url = 'main:login'


class TVShowDeleteView(DeleteView):
    model = TVShows
    success_url = reverse_lazy('main:account')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ChannelShowTimeCreateView(LoginRequiredMixin, CreateView):
    model = ChannelShowTime
    form_class = ChannelShowTimeForm
    template_name = 'channelshowtime_form.html'
    success_url = reverse_lazy('main:account')
    login_url = 'main:login'


class ChannelShowTimeUpdateView(LoginRequiredMixin, UpdateView):
    model = ChannelShowTime
    form_class = ChannelShowTimeForm
    template_name = 'channelshowtime_form.html'
    success_url = reverse_lazy('main:account')
    login_url = 'main:login'


class ChannelShowTimeDeleteView(DeleteView):
    model = ChannelShowTime
    success_url = reverse_lazy('main:account')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AccountView(TemplateView):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        context['channels'] = Channels.objects.all()
        context['shows'] = TVShows.objects.all()
        context['channel_showtimes'] = ChannelShowTime.objects.select_related('channel', 'show').all()

        return context
