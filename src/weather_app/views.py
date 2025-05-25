# Create your views here.
from django.shortcuts import render
from django.views import View


class WeatherAppView(View):
    template_name = 'weather_app/index.html'

    def get(self, request):
        return render(request, self.template_name)
