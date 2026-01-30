from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Habit, DailyEntry, Quote
import json
from urllib.request import urlopen

# ==========================================
# 1. MAIN APP LOGIC (Fixed Grid, Time, Name)
# ==========================================
def daily_tracker(request):
    # --- A. India Time Setup ---
    utc_now = timezone.now()
    india_time = utc_now + timedelta(hours=5, minutes=30)
    today = india_time.date()
    
    # --- B. Greeting Logic ---
    current_hour = india_time.hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    # --- C. Date Selection ---
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    # --- D. Habits Data ---
    habits = Habit.objects.all()
    completed_habit_ids = []
    if DailyEntry.objects.filter(date=selected_date).exists():
        entry = DailyEntry.objects.get(date=selected_date)
        completed_habit_ids = list(entry.habits_completed.values_list('id', flat=True))

    # --- E. Grid Logic (Last 30 Days) ---
    history = []
    for i in range(29, -1, -1): # Past 30 days
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

    # --- F. Calendar Strip ---
    date_list = []
    for i in range(14, -3, -1): # Past 14 days + Next 2 days
        d = today - timedelta(days=i)
        date_list.append(d)

    # --- G. Random Quote ---
    quote = Quote.objects.order_by('?').first()
    if not quote:
        quote = Quote(text="Likho kam, Padho jyada!!", author="Muntazir")

    # --- H. Stats Unlock Logic ---
    show_stats = False
    target_date = datetime.strptime("2026-02-07", "%Y-%m-%d").date()
    if today >= target_date:
        show_stats = True

    context = {
        'habits': habits,
        'completed_ids': completed_habit_ids,
        'selected_date': selected_date,
        'today': today,
        'greeting': greeting,
        'username': "Aalok",   # <-- Aapka Naam
        'date_list': date_list,
        'history': history,
        'show_stats': show_stats,
        'quote': quote
    }
    return render(request, 'tracker/index.html', context)


# ==========================================
# 2. HELPER FUNCTIONS (To Fix Build Error)
# ==========================================

def create_superuser_view(request):
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            return HttpResponse("✅ Success! User: <b>admin</b> | Password: <b>admin123</b> created.")
        else:
            return HttpResponse("⚠️ Admin user already exists. Go to /admin to login.")
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}")

def populate_quotes(request):
    url = "https://dummyjson.com/quotes?limit=50"
    try:
        response = urlopen(url)
        data = json.loads(response.read())
        count = 0
        for item in data['quotes']:
            if not Quote.objects.filter(text=item['quote']).exists():
                Quote.objects.create(text=item['quote'], author=item['author'])
                count += 1
        return HttpResponse(f"<h1>🚀 Done!</h1><p>Added {count} quotes.</p>")
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}")