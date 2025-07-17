from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Quote(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]  

# class DiaryEntry(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
#     content = models.TextField()
#     date = models.DateField(default=date.today)

#     class Meta:
#         unique_together = ('user', 'date')  # Ensures one entry per user per date

#     def __str__(self):
#         return self.content[:30]
    
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Goal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_term_goal = models.CharField(max_length=255, blank=True, null=True)
    long_term_goal = models.CharField(max_length=255, blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    goal_target_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Goals"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


from django.db import models
from django.contrib.auth.models import User

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.JSONField(default=list)
