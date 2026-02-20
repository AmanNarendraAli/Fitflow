from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Gym(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    code = models.CharField(unique=True, max_length=6)
    def save(self, *args, **kwargs): #overriding the save method to generate a random code
        if not self.code:
            # Keep trying until we find a code that isn't in the database
            while True:
                new_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if not Gym.objects.filter(code=new_code).exists():
                    self.code = new_code
                    break
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class User(AbstractUser):
    OWNER = 'OWNER'
    STAFF = 'STAFF'
    TRAINER = 'TRAINER'
    MEMBER = 'MEMBER'
    
    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (STAFF, 'Staff'),
        (TRAINER, 'Trainer'),
        (MEMBER, 'Member'),
    ]

    role = models.CharField(max_length = 10, choices = ROLE_CHOICES, default = MEMBER) 
    gym = models.ForeignKey(Gym, on_delete = models.CASCADE, null = True, blank = True) #gym id is a foreign key in user table
    def __str__(self):
        return (f"{self.username} - {self.role}")

class TrainerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='trainer_profile')
    gym = models.ForeignKey(Gym, on_delete = models.CASCADE, null = True, blank = True)
    bio = models.TextField(blank=True)
    specialties = models.CharField(max_length=100)
    def __str__(self):
        return (f"Trainer {self.user.username}")

class MemberProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='member_profile')
    gym = models.ForeignKey(Gym, on_delete = models.CASCADE, null = True, blank = True)
    phone = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.TRAINER:
            TrainerProfile.objects.create(user=instance, gym=instance.gym)
        elif instance.role == User.MEMBER:
            MemberProfile.objects.create(user=instance, gym=instance.gym)