from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Gym(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    code = models.CharField(unique=True, max_length=10)
    class Meta:
        db_table = "Gym"
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
    class Meta:
        db_table = "User"
    def __str__(self):
        return (f"{self.username} - {self.role}")