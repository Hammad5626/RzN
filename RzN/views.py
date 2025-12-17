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
                    time_class = "danger-time"
                elif 0 <= hour < 2 or 5 <= hour < 7:
                    time_class = "warning-time"
                else:
                    time_class = ""

                converted_times.append({
                    'name': p.name,
                    'hq': p.hq_level,
                    'power': p.power,
                    'country': p.country,
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

def players(request):
    sort = request.GET.get('sort')
    qs = Player.objects.select_related('country', 'timezone')

    if sort == 'power':
        qs = qs.order_by('-power')
    elif sort == 'hq':
        qs = qs.order_by('-hq_level')
    elif sort == 'name':
        qs = qs.order_by('name')
    elif sort == 'active':
        qs = qs.order_by('-is_active')
    elif sort == 'key':
        qs = qs.order_by('-is_key_player')

    return render(request, 'players.html', {'players': qs})


def edit_player(request, pk):
    player = Player.objects.get(pk=pk)
    countries = Country.objects.all().order_by('name')

    if request.method == 'POST':
        player.name = request.POST['name']
        player.hq_level = request.POST['hq_level']
        player.power = request.POST['power']
        player.country_id = request.POST['country']
        player.timezone_id = request.POST.get('timezone')
        player.is_active = 'is_active' in request.POST
        player.is_key_player = 'is_key_player' in request.POST
        player.save()

        return redirect('players')

    return render(request, 'edit_player.html', {
        'player': player,
        'countries': countries
    })

def delete_player(request, pk):
    if request.method == 'POST':
        Player.objects.filter(pk=pk).delete()
    return redirect('players')
