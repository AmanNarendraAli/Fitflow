from django.db import models

# Create your models here.
class Room(models.Model):
    gym = models.ForeignKey('accounts.Gym',on_delete=models.CASCADE,related_name="rooms")
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(help_text="Max no. of people allowed")
    class Meta:
        constraints = [models.UniqueConstraint(fields=['gym','name'], name='unique_room_per_gym')]
    def __str__(self):
        return f"{self.name} ({self.gym.name})"

    