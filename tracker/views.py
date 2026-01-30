from django.shortcuts import render, redirect
from .models import Habit, DailyEntry, Quote
from datetime import date, timedelta, datetime # datetime import kiya greeting ke liye
import random

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
    today = date.today()
    
    # --- 1. SMART GREETING LOGIC ---
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning, Aalok"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon, Aalok"
    elif 17 <= current_hour < 22:
        greeting = "Good Evening, Aalok"
    else:
        greeting = "Hustling Late, Aalok?"

    # --- 2. HANDLE DAILY ENTRIES ---
    habits = Habit.objects.filter(is_active=True).order_by('priority')
    for habit in habits:
        DailyEntry.objects.get_or_create(habit=habit, date=today)

    if request.method == "POST":
        entry_id = request.POST.get('entry_id')
        entry = DailyEntry.objects.get(id=entry_id)
        if entry.habit.habit_type == 'BOOL':
            entry.value_bool = not entry.value_bool
        elif entry.habit.habit_type == 'INT':
            entry.value_int = request.POST.get('value_int', 0)
        elif entry.habit.habit_type == 'TEXT':
            entry.value_text = request.POST.get('value_text', '')
        entry.save()
        return redirect('tracker')

    # --- 3. PREPARE DATA ---
    entries = DailyEntry.objects.filter(date=today).order_by('habit__priority')
    daily_data = []
    for entry in entries:
        streak = 0
        past_entries = DailyEntry.objects.filter(habit=entry.habit, date__lt=today).order_by('-date')
        for p in past_entries:
            if p.value_bool or p.value_int > 0 or p.value_text:
                streak += 1
            else:
                break
        daily_data.append({'entry': entry, 'streak': streak})

   # --- 4. COMPACT HEATMAP (Last 30 days for 6x5 Grid) ---
    heatmap_data = []
    # Start from 29 days ago so we end exactly on today (Total 30 days)
    start_date = today - timedelta(days=29) # <-- CHANGED FROM 34 TO 29
    
    for i in range(30): # <-- CHANGED FROM 35 TO 30 (6 Rows x 5 Columns)
        current_day = start_date + timedelta(days=i)
        score = get_daily_score(current_day)
        
        # Color Logic (Same as before)
        color = "bg-gray-800"
        if score > 0: color = "bg-green-900"
        if score > 40: color = "bg-green-600"
        if score > 80: color = "bg-green-400"
        
        heatmap_data.append({
            'date': current_day,
            'color': color,
            'is_today': current_day == today,
            'score': score
        })

    # --- 5. LOCAL QUOTE (Fallback) ---
    quotes = Quote.objects.all()
    random_quote = random.choice(quotes) if quotes.exists() else None

    return render(request, 'tracker/index.html', {
        'daily_data': daily_data,
        'heatmap_data': heatmap_data,
        'quote': random_quote,
        'today': today,
        'greeting': greeting, # <-- Sending greeting to template
    })