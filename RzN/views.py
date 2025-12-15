from django.shortcuts import render, redirect
from .models import Player, Country, Timezone
from datetime import datetime, timezone, time, timedelta
from django.http import JsonResponse

def home(request):
    converted_times = []
    selected_time_str = None

    players = Player.objects.select_related('country', 'timezone')

    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        if date_str and time_str:
            utc_dt = datetime.strptime(
                f"{date_str} {time_str}",
                "%Y-%m-%d %H:%M"
            ).replace(tzinfo=timezone.utc)

            selected_time_str = utc_dt.strftime("%Y-%m-%d %H:%M UTC+00")

            for p in players:
                offset_seconds = p.timezone.gmt_offset
                local_dt = utc_dt + timedelta(seconds=offset_seconds)
                hour = local_dt.hour

                if 2 <= hour < 5:
                    time_class = "bg-danger text-white"
                elif 0 <= hour < 2 or 5 <= hour < 7:
                    time_class = "bg-warning"
                else:
                    time_class = ""

                converted_times.append({
                    'name': p.name,
                    'power': p.power,
                    'country': p.country.name,
                    'local_time': local_dt.strftime("%Y-%m-%d %H:%M"),
                    'time_class': time_class,
                })

    return render(request, "home.html", {
        "converted_times": converted_times,
        "selected_time": selected_time_str,
    })



def add_player(request):
    countries = Country.objects.all().order_by('name')

    if request.method == 'POST':
        name = request.POST['name']
        hq_level = request.POST['hq_level']
        power = request.POST['power']
        country_id = request.POST['country']
        tz_id = request.POST.get('timezone')

        country = Country.objects.get(id=country_id)
        if tz_id:
            timezone = Timezone.objects.get(id=tz_id)
        else:
            # if only one timezone exists, take it automatically
            timezone = country.timezones.first()

        Player.objects.create(
            name=name,
            hq_level=hq_level,
            power=power,
            country=country,
            timezone=timezone,
            is_active='is_active' in request.POST,
            is_key_player='is_key_player' in request.POST
        )

        return redirect('home')

    return render(request, 'add_player.html', {'countries': countries})

def country_timezones(request, country_id):
    country = Country.objects.get(id=country_id)
    tzs = list(country.timezones.values('id', 'zone_name', 'gmt_offset', 'gmt_offset_name'))
    return JsonResponse(tzs, safe=False)

