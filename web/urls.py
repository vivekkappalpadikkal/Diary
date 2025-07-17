from django.urls import path
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import dentry, save_diary_entry, get_diary_entry
from django.contrib.auth import views as auth_views



urlpatterns = [ 
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('wrapup/', views.wrapup, name='wrapup'),
    path('dentry/', views.dentry, name='dentry'),
    # path('quotes/', views.quote_list, name='quote_list')
      # To load the diary entry page with a specific date
    path('save-entry/', views.save_diary_entry, name='save_entry'),  # To save the diary entry
    path('upload-profile-pic/', views.upload_profile_pic, name='upload_profile_pic'),
    path('profile/', views.profile, name='profile'),
    path('delete-profile-pic/', views.delete_profile_picture, name='delete_profile_picture'),#abhishek
    path('entry/<str:date>/', views.entry_by_date, name='entry_by_date'),
    
    path("dentry/", dentry, name="dentry"),
    path("save-diary-entry/", save_diary_entry, name="save_diary_entry"),
    path("get-diary-entry/", get_diary_entry, name="get_diary_entry"),
    #path('', views.home, name='home'),
    path('api/recent-diaries/', views.recent_diaries, name='recent_diaries'),
    path('api/entry/', views.get_entry_by_date, name='get_entry_by_date'),
    path('api/recent-diaries/', views.recent_diaries, name='recent_diaries'),
    path('home', views.todo_view, name='todo'),
    path('save-todos/', views.save_todos, name='save_todos'),
    path('get-todos/', views.get_todos, name='get_todos'),
    
   
     # Reset password...
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='web/reset_password.html'
    ), name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='web/reset_password_sent.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='web/reset_password_confirm.html'
    ), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='web/reset_password_complete.html'
    ), name='password_reset_complete'),
    

path('weekly-wrapup/', views.weekly_wrapup, name='weekly_wrapup'),

       

  
    
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)