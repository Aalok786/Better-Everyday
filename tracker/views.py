from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Habit, DailyEntry, Quote

def daily_tracker(request):
    # 1. India Time Setup (UTC + 5:30 manually)
    utc_now = timezone.now()
    india_time = utc_now + timedelta(hours=5, minutes=30)
    today = india_time.date()
    
    # 2. Greeting Logic
    current_hour = india_time.hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    # 3. Date Selection Logic
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    # 4. Habits Data
    habits = Habit.objects.all()
    completed_habit_ids = []
    if DailyEntry.objects.filter(date=selected_date).exists():
        entry = DailyEntry.objects.get(date=selected_date)
        completed_habit_ids = list(entry.habits_completed.values_list('id', flat=True))

    # 5. Grid Logic (Last 30 Days) - YE PART GRID DIKHAYEGA
    history = []
    for i in range(29, -1, -1):
        d = today - timedelta(days=i)
        
        total_habits = habits.count()
        percent = 0
        if total_habits > 0:
            entries = DailyEntry.objects.filter(date=d)
            if entries.exists():
                done = entries.first().habits_completed.count()
                percent = int((done / total_habits) * 100)
        
        history.append({
            'date': d, 
            'percent': percent,
            'is_today': (d == today)
        })

    # 6. Calendar Strip Logic
    date_list = []
    for i in range(14, -2, -1): # Past 14 days + Next 2 days
        d = today - timedelta(days=i)
        date_list.append(d)

    # 7. Quote Logic
    quote = Quote.objects.order_by('?').first()
    if not quote:
        quote = Quote(text="Likho kam, Padho jyada!!", author="Muntazir")

    # 8. Stats Logic
    show_stats = False
    target_date = datetime.strptime("2026-02-07", "%Y-%m-%d").date()
    if today >= target_date:
        show_stats = True

    # FINAL DATA PACKET (Ye HTML ke paas jayega)
    context = {
        'habits': habits,
        'completed_ids': completed_habit_ids,
        'selected_date': selected_date,
        'today': today,          # <-- Date Box ke liye
        'greeting': greeting,    # <-- Greeting ke liye
        'username': "Aalok",     # <-- Naam ke liye
        'date_list': date_list,
        'history': history,      # <-- Grid ke liye
        'show_stats': show_stats,
        'quote': quote
    }
    
    return render(request, 'tracker/index.html', context)