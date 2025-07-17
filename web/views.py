from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import markdown

from .utils.gemini import generate_weekly_wrapup
from .models import Quote
import hashlib
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from .models import DiaryEntry, UserProfile, TodoList
from django.utils import timezone
from datetime import datetime, date, timedelta
import json
from .models import UserProfile
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from .models import Goal
from .forms import GoalForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Quote, DiaryEntry, UserProfile, TodoList, Goal
from django.http import JsonResponse
# from datetime import datetime, date, timedelta
import json
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from .forms import GoalForm
from django.contrib.auth.decorators import login_required
import hashlib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import os
import nltk
import os
from nltk.data import path as nltk_path

# Set a safe location to store nltk data
nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")

# Add it to nltk's search path
nltk_path.append(nltk_data_path)

# Download if not already downloaded
nltk.download('vader_lexicon', download_dir=nltk_data_path)

# Get the NLTK data path (where you downloaded the data)
# nltk_data_path = "C:\\Users\\Admin\\AppData\\Roaming\\nltk_data"  # <--- IMPORTANT: Use the path from your previous output!

# Add the path to NLTK's search locations
# nltk.data.path.append(nltk_data_path)

# Download the necessary NLTK data (punkt and stopwords) -  KEEP THIS, it ensures data is there.
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading punkt data...")  # Add a print statement
    nltk.download('punkt', download_dir=nltk_data_path)  # Explicitly specify download location

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading stopwords data...")
    nltk.download('stopwords', download_dir=nltk_data_path)

try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    print("Downloading vader_lexicon data...")
    nltk.download('vader_lexicon', download_dir=nltk_data_path)


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Here you'd typically send an email with a reset link.
            messages.success(request, 'A password reset link has been sent to your email.')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
        return redirect('reset_password')

    return render(request, 'web/reset_password.html')



@login_required
def home(request):
    profile_pics = UserProfile.objects.filter(user=request.user).first()

    if profile_pics and profile_pics.profile_picture and profile_pics.profile_picture.name:
        profile_pic_url = profile_pics.profile_picture.url
    else:
        profile_pic_url = "https://static-00.iconduck.com/assets.00/profile-major-icon-512x512-xosjbbdq.png"

    quote = get_daily_quote()
     # ✅ Fetch latest 4 diary entries for the current user
    recent_entries = DiaryEntry.objects.filter(user=request.user).order_by('-date')[:4]

    return render(request, 'web/home.html', {
        'quote': quote,
        'profile_pics': profile_pics,
        'profile_pic_url': profile_pic_url,
        'recent_entries': recent_entries,  # Pass to template
    })
def delete_profile_picture(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile
        if user_profile.profile_picture:
            user_profile.profile_picture.delete(save=False)  # Deletes file from media
            user_profile.profile_picture = None
            user_profile.save()
            return JsonResponse({'message': 'Profile picture deleted successfully.'})
        return JsonResponse({'error': 'No picture to delete.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def login_view(request):
    quote = get_daily_quote()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, 'web/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Logs the user in
            return redirect('home')  # Assuming you have a path named 'home'
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'web/login.html')

    return render(request, 'web/login.html',{'quote': quote})

def signup(request):
    quote = get_daily_quote()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        

        if password != confirm_password:
            messages.error(request, "Passwords do not match.") 
            return render(request, 'web/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'web/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'web/signup.html')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return render(request, 'web/login.html', {'username': username})
    
    return render(request, 'web/signup.html', {'quote': quote})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

def about(request):
    return render(request, 'web/about.html')

def profile(request):
    return render(request, 'web/profile.html')

def wrapup(request):
    return render(request, 'web/wrapup.html')

def dentry(request):
    return render(request, 'web/dentry.html')

def get_daily_quote():
    quotes = list(Quote.objects.all())
    if not quotes:
        return None

    today_str = date.today().isoformat()

    hash_val = int(hashlib.sha256(today_str.encode()).hexdigest(), 16)
    index = hash_val % len(quotes)
    return quotes[index]

def save_diary_entry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data from fetch
            print("Received:", data)  # ✅ DEBUG: Prints data to your Django server console

            content = data.get('content')
            date = data.get('date')

            if content and date:
                selected_date = datetime.strptime(date, '%Y-%m-%d').date()
                DiaryEntry.objects.update_or_create(
                    date=selected_date, defaults={'content': content}
                )
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Missing content or date'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def upload_profile_pic(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        return JsonResponse({"message": user_profile.profile_picture.url})
    return JsonResponse({"error": "No image uploaded"}, status=400)

def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

def profile(request):
    user = request.user
    goal,created = Goal.objects.get_or_create(user=user)

    if request.method == 'POST':
        goal.short_term_goal = request.POST.get('short_term_goal', '')
        goal.long_term_goal = request.POST.get('long_term_goal', '')
        goal.hobbies = request.POST.get('hobbies', '')
        goal.goal_target_date = request.POST.get('goal_target_date') or None
        goal.save()
        return redirect('profile')  # reload to display updated info

    context = {
        'user': user,
        'goal': goal,
    }
    return render(request, 'web/profile.html', context)


@login_required
def entry_by_date(request, date):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return render(request, 'invalid_date.html', {'date': date})  # optional

    entry, created = DiaryEntry.objects.get_or_create(user=request.user, date=date_obj)

    if request.method == 'POST':
        entry.content = request.POST.get('content', '')
        entry.save()
        return redirect('entry_by_date', date=date)

    return render(request, 'web/dentry.html', {'entry': entry, 'date': date_obj})





import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from .models import DiaryEntry

def dentry(request):
    return render(request, 'web/dentry.html')

# Fetch diary entry for a given date
def get_diary_entry(request):
    if request.method == "GET":
        date = request.GET.get("date")
        if date:
            try:
                entry = DiaryEntry.objects.filter(date=date).first()
                if entry:
                    return JsonResponse({"status": "success", "content": entry.content})
                else:
                    return JsonResponse({"status": "success", "content": ""})  # No entry found
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"})

# Save diary entry
def save_diary_entry(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content")
            date = data.get("date")

            if content and date:
                selected_date = datetime.strptime(date, "%Y-%m-%d").date()
                DiaryEntry.objects.update_or_create(
    user=request.user,
    date=selected_date,
    defaults={'content': content}
)

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Missing content or date"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"})



@login_required
def recent_diaries(request):
    recent_entries = DiaryEntry.objects.filter(user=request.user).order_by('-date')[:5]
    data = [
        {
            'content': entry.content[:100],  # Show a preview (limit to 100 chars)
            'date': entry.date.strftime('%Y-%m-%d'),
        }
        for entry in recent_entries
    ]
    return JsonResponse(data, safe=False)


def get_entry_by_date(request):
    date_str = request.GET.get('date')
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        entry = DiaryEntry.objects.filter(user=request.user, date=date_obj).first()
        return JsonResponse({'content': entry.content if entry else ''})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
@login_required
def save_todos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tasks = data.get('tasks', [])

        todo, created = TodoList.objects.get_or_create(user=request.user)
        todo.tasks = tasks
        todo.save()

        return JsonResponse({'status': 'saved'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def todo_view(request):
    todo, created = TodoList.objects.get_or_create(user=request.user)
    return render(request, 'todo.html', {'tasks': todo.tasks})


@login_required
def get_todos(request):
    todo, created = TodoList.objects.get_or_create(user=request.user)
    return JsonResponse({'tasks': todo.tasks})




@login_required
def recent_diaries(request):
    entries = (
        DiaryEntry.objects.filter(user=request.user)
        .order_by('-date')[:5]
    )

    data = [
        {"date": entry.date.strftime("%Y-%m-%d"), "content": entry.content[:100]}
        for entry in entries
    ]

    return JsonResponse(data, safe=False)

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Here you'd typically send an email with a reset link.
            messages.success(request, 'A password reset link has been sent to your email.')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
        return redirect('reset_password')

    return render(request, 'reset_password.html')

def reset_password(request):
    return render(request, 'web/reset_password.html')



def extract_keywords(text):
    """
    Extracts keywords from a given text, removing stop words and punctuation.

    Args:
        text (str): The text to extract keywords from.

    Returns:
        list: A list of keywords.
    """
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [w for w in words if not w in stop_words and w.isalnum()]
    return filtered_words


def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using NLTK's VADER.

    Args:
        text (str): The text to analyze.

    Returns:
        float: The compound sentiment score (-1 to 1, where -1 is most negative, 1 is most positive).
    """
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    return vs['compound']



def wrapup(request):
    print(f"NLTK data path: {nltk.data.path}") # Print the NLTK data path
    """
    Generates a weekly wrap-up of diary entries, including goal analysis and sentiment.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered wrap-up page.
    """
    user = request.user
    today = datetime.today().date()
    # Calculate the date range for the past week
    start_date = today - timedelta(days=7)
    end_date = today

    # Fetch diary entries for the past week
    diary_entries = DiaryEntry.objects.filter(
        user=user, date__range=[start_date, end_date]
    ).order_by('date')

    # Fetch user's goals
    # goal = Goal.objects.get(user=user)  # Assuming one Goal per user
    goal = Goal.objects.filter(user=user).first()

    # 1. Analyze Goals and Extract Keywords
    goal_keywords = (
        extract_keywords(goal.short_term_goal + " " + goal.long_term_goal)
        if goal
        else []
    )

    # 2. Analyze Diary Entries
    entries_data = []
    goal_related_count = 0  # Count of entries related to goals
    total_sentiment = 0

    for entry in diary_entries:
        entry_keywords = extract_keywords(entry.content)
        # Check for goal relevance (Improved logic)
        relevant_keywords = [
            word for word in entry_keywords if word in goal_keywords
        ]
        if relevant_keywords:
            goal_related_count += 1
        sentiment_score = analyze_sentiment(entry.content)
        total_sentiment += sentiment_score
        entries_data.append(
            {
                'date': entry.date,
                'content': entry.content,
                'sentiment_score': sentiment_score,
                'relevant_keywords': relevant_keywords,  # Pass the relevant keywords
            }
        )
    # Calculate average sentiment
    average_sentiment = (
        total_sentiment / len(diary_entries) if diary_entries else 0
    )
    # Prepare context for the template
    context = {
        'goal': goal,
        'entries_data': entries_data,
        'goal_related_count': goal_related_count,
        'total_entries': len(diary_entries),
        'average_sentiment': average_sentiment,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'web/wrapup.html', context)


def weekly_wrapup(request):
    user = request.user
    today = timezone.now().date()
    week_start = today - timedelta(days=7)

    # Get diary entries from the past week
    entries = DiaryEntry.objects.filter(user=user, date__range=[week_start, today]).order_by('date')

    # Get the user's goals (only one per user as per model)
    try:
        goal = Goal.objects.get(user=user)
        goal_text = f"Short-term Goal: {goal.short_term_goal or 'N/A'}\n" \
                    f"Long-term Goal: {goal.long_term_goal or 'N/A'}\n" \
                    f"Hobbies: {goal.hobbies or 'N/A'}\n" \
                    f"Target Date: {goal.goal_target_date or 'N/A'}"
    except Goal.DoesNotExist:
        goal_text = "No goal set."

    # Combine diary text
    diary_text = "\n\n".join([f"{entry.date}:\n{entry.content}" for entry in entries])

    # Call Gemini AI to generate wrap-up
    wrapup = generate_weekly_wrapup(diary_text, goal_text)
    wrapup_html = markdown.markdown(wrapup)


    return render(request, 'web/weekly_wrapup.html', {
        'wrapup': wrapup_html,
        'week_start': week_start,
        'week_end': today,
        'entries': entries
    })
    