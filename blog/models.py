from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    friend = models.ManyToManyField(User, blank=True, related_name='friend')
    blocked_user = models.ManyToManyField(
        User, blank=True, related_name='blockeduser')
    is_private = models.BooleanField(default=False)
    # friend_request = models.ForeignKey(Friend_Request, related_name='friend_request')

    def __str__(self):
        return self.user.username


class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return 'to_user: ' + self.to_user.username + ' & from_user: ' + self.from_user.username

    @classmethod
    def all_friend_requests(self):
        return self.objects.all()

    @classmethod
    def user_friend_requests(self, user):
        return self.objects.filter(to_user=user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
