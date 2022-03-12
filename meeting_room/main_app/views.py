from django.shortcuts import render, redirect
from .models import Events
from .forms import CreateForm
from datetime import datetime, timedelta, date
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate, logout
import pandas 


#creating new booking
def new_booking(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            start_time = datetime.strptime(request.POST['start_time'], "%d-%m-%Y %H:%M")
            end_time = datetime.strptime(request.POST['end_time'], "%d-%m-%Y %H:%M")
            duration = end_time - start_time
            if start_time < datetime.now(): #checking the correctness of the data
                error = 'Некорректная дата или время'
                return render(request, 'main_app/new_booking.html', {'error': error, 'form': form}) 
            elif start_time > end_time:
                error = 'Некорректные даты или время'
                return render(request, 'main_app/new_booking.html', {'error': error, 'form': form})            
            elif duration < timedelta(minutes=30):
                error = 'Бронирование не может быть меньше 30 минут'
                return render(request, 'main_app/new_booking.html', {'error': error, 'form': form})
            elif duration > timedelta(hours=24 ,minutes=30):
                error = 'Бронирование не может быть больше 24 часов'
                return render(request, 'main_app/new_booking.html', {'error': error, 'form': form}) 
            another_events = Events.objects.filter(start_time__lte=start_time, end_time__gte=start_time)|Events.objects.filter(start_time__lte=end_time, end_time__gte=end_time)|Events.objects.filter(start_time__gte=start_time, end_time__lte=end_time)
            if another_events:
                error = 'В выбранное время переговорка уже занята. Выберите другое время'
                return render(request, 'main_app/new_booking.html', {'error': error, 'form': form}) 
            event = Events.objects.create(user=request.user, title=title, description=description, start_time=start_time, end_time=end_time, duration=duration)
            event.save()
            success = 'Переговорка успешно забронирована'
    else:
        form = CreateForm()
        success = ''
    return render(request, 'main_app/new_booking.html', {'form': form, 'success': success,})

#remove a reservation
def event_remove(request,event_id): 
    event = Events.objects.get(id=event_id)
    if event.user == request.user:
        event.delete()
    return redirect('index')


#get information about the event
def event_detail(request, event_id):
    try:
        event = Events.objects.get(id=event_id)
    except Exception as e:
        raise e
    return render(request, 'main_app/event_detail.html', {'event':event})


def loginView(request): 
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None: 
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'main_app/login.html', {'form': form})
        else:
    
            return render(request, 'main_app/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'main_app/login.html', {'form': form})


def logoutView(request):
    logout(request) 
    return redirect('login')


#main page
def calendar(request, year, week_number):
    week = [date.fromisocalendar(year,week_number,x) for x in range (1,8) ]
    # events = Events.objects.filter(start_time__range=[week[0], week[6]])|Events.objects.filter(end_time__range=[week[0], week[6]])
    events = Events.objects.filter(start_time__gte=week[0], start_time__lte=week[6])|Events.objects.filter(end_time__gte=week[0], end_time__lte=week[6])
    hours = pandas.date_range("00:00", "00:24", freq="01min").strftime('%H:%M')
    return render(request, 'main_app/calendar.html', {'week': week, 'year':year, 'week_number':week_number, 'events':events, 'hours':hours})


#get today's week
def index(request):
    year_today = date.today().isocalendar()[0]
    week_today = date.today().isocalendar()[1]
    return calendar(request, year_today, week_today)


# get another week
def another_week(request, action, year, week_number):
    if action == 'prev':
        week = week_number - 1
        if week == 0:
            week = 52
            year -= 1
    elif action == 'next':
        week = week_number + 1
        if week == 52:
            week = 1
            year += 1
    return calendar(request, year, week)