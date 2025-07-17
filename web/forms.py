# forms.py
from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['short_term_goal', 'long_term_goal', 'hobbies', 'goal_target_date']
