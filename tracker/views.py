from django.shortcuts import render, redirect
from .models import Habit, DailyEntry, Quote, DailyEntry
from datetime import date, timedelta, datetime # datetime import kiya greeting ke liye
import random, json 
from urllib.request import urlopen
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone

def calculate_streak(habit):
    """
    Ye function check karta hai ki lagatar kitne din se habit complete hui hai.
    """
    streak = 0
    today = date.today()
    # Pichle saare din check karna (aaj se peeche)
    entries = DailyEntry.objects.filter(habit=habit, date__lt=today).order_by('-date')
    
    for entry in entries:
        if entry.value_bool or entry.value_int > 0 or entry.value_text:
            streak += 1
        else:
            break # Jahan chain tooti, wahan streak khatam
    return streak

# Helper function to calculate daily completion percentage
def get_daily_score(selected_date):
    active_habits = Habit.objects.filter(is_active=True).count()
    if active_habits == 0:
        return 0
    
    # Count completed entries for that date
    entries = DailyEntry.objects.filter(date=selected_date)
    completed = 0
    for entry in entries:
        if entry.value_bool:
            completed += 1
        elif entry.habit.habit_type == 'INT' and entry.value_int > 0:
            completed += 1
        elif entry.habit.habit_type == 'TEXT' and entry.value_text:
            completed += 1
            
    return int((completed / active_habits) * 100)

# ... (get_daily_score function waisa hi rahega) ...

def daily_tracker(request):
    # 1. Date Selection Logic
    today = timezone.now().date()
    selected_date_str = request.GET.get('date') # URL se date uthao (?date=2026-01-20)
    
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    else:
        selected_date = today

    # Future Date Protection (Future mein jane se roko)
    if selected_date > today:
        return redirect('tracker')

    # 2. Calendar Strip Data (Pichle 30 din ki list)
    date_list = []
    for i in range(30): # Last 30 days
        d = today - timedelta(days=i)
        date_list.append(d)
    
    # 3. Habits & Data Fetching for Selected Date
    habits = Habit.objects.all()
    
    # User ne us din kya tick kiya tha?
    completed_habit_ids = []
    try:
        entry = DailyEntry.objects.get(date=selected_date)
        completed_habit_ids = list(entry.habits_completed.values_list('id', flat=True))
    except DailyEntry.DoesNotExist:
        entry = None

    # 4. Grid Logic (Home Page Consistency)
    # (Ye purana logic hi hai, bas ab link banayega)
    history = []
    start_date = today - timedelta(days=29) # Grid start
    for i in range(30):
        d = start_date + timedelta(days=i)
        try:
            e = DailyEntry.objects.get(date=d)
            total = habits.count()
            done = e.habits_completed.count()
            percent = int((done / total) * 100) if total > 0 else 0
        except DailyEntry.DoesNotExist:
            percent = 0
        
        history.append({
            'date': d, 
            'percent': percent,
            'is_today': (d == today)
        })

    # 5. Stats Logic (Auto-Switch after Feb 7th)
    show_stats = False
    target_date = datetime.strptime("2026-02-07", "%Y-%m-%d").date()
    if today >= target_date:
        show_stats = True

    return render(request, 'tracker/index.html', {
        'habits': habits,
        'completed_ids': completed_habit_ids,
        'selected_date': selected_date,
        'today': today,
        'date_list': date_list,   # Calendar ke liye
        'history': history,       # Grid ke liye
        'show_stats': show_stats, # Stats toggle ke liye
        'quote': Quote.objects.order_by('?').first()
    })

# File ke sabse neeche ye paste karein:
def create_superuser_view(request):
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            return HttpResponse("✅ Success! User: <b>admin</b> | Password: <b>admin123</b> created.")
        else:
            return HttpResponse("⚠️ Admin user already exists. Go to /admin to login.")
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}")
    
    # 1. Ye Naya "Bulk Loader" Function (150 Quotes wala)
def populate_quotes(request):
    # Ye ek free API hai jo 150 quality quotes deti hai
    url = "https://dummyjson.com/quotes?limit=150"
    
    try:
        response = urlopen(url)
        data = json.loads(response.read())
        
        count = 0
        for item in data['quotes']:
            # API se data nikal kar apne style mein map kar rahe hain
            quote_text = item['quote']
            quote_author = item['author']
            
            # Check duplicate (taaki baar baar same save na ho)
            if not Quote.objects.filter(text=quote_text).exists():
                Quote.objects.create(text=quote_text, author=quote_author)
                count += 1
                
        return HttpResponse(f"<h1>🚀 Done!</h1><p>Successfully downloaded and added <b>{count}</b> new quotes to your database.</p>")
    
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}")

# 2. Ye apka Main Home Page Logic (Isme 'Random' logic check kar lein)
def daily_tracker(request):
    # Random Logic: order_by('?') ka matlab hai 'Randomly Pick Karo'
    # Ye apne aap loop mein chalta rahega (har refresh par naya)
    random_quote = Quote.objects.order_by('?').first()
    
    if not random_quote:
        # Agar DB khali hai to Fallback
        random_quote = Quote(text="Likho kam, Padho jyada!!", author="Muntazir")

    # Baaki aapka purana logic...
    habits = Habit.objects.all()
    # ... (baaki context wagera same rakhein) ...
    
    return render(request, 'tracker/index.html', {
        'habits': habits,
        'quote': random_quote, # <-- Ye template me jayega
        # ... baaki context ...
    })