from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    TYPE_CHOICES = [
        ('BOOL', 'Checkbox (Yes/No)'),
        ('INT', 'Numeric (Hours/Glasses)'),
        ('TEXT', 'Journal (What I Learnt)'),
    ]
    
    name = models.CharField(max_length=100)
    habit_type = models.CharField(max_length=5, choices=TYPE_CHOICES, default='BOOL')
    priority = models.IntegerField(default=0)  # <-- Ye naya field hai
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['priority'] # <-- Isse habits hamesha priority ke hisab se dikhengi

    def __str__(self):
        return f"{self.priority} - {self.name}"

class DailyEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    # These fields store the actual data for each day
    value_bool = models.BooleanField(default=False)
    value_int = models.IntegerField(default=0)
    value_text = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('habit', 'date') # Prevents duplicate entries for the same day

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=200, blank=True, null=True)
    book_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.text[:30]}..."'