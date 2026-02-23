from django.db import models

# Create your models here.
# `ClassType`: `gym`, `name`, `duration_minutes`, `default_capacity`
# `ClassSession`: `gym`, `class_type`, `trainer`, `room` (optional), `starts_at`, `ends_at`, `capacity`, `status`

class ClassType(models.Model):
    gym = models.ForeignKey('accounts.Gym',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    default_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.gym.name} - {self.name}"

class ClassSession(models.Model):
    gym = models.ForeignKey('accounts.Gym',on_delete=models.CASCADE)
    class_type = models.ForeignKey(ClassType,on_delete=models.CASCADE)
    trainer = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    room = models.ForeignKey('gyms.Room',on_delete=models.CASCADE,null=True,blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    capacity = models.IntegerField()
    status = models.CharField(max_length=20,choices=[('SCHEDULED','Scheduled'),('CANCELLED','Cancelled'),('COMPLETED','Completed')])

    def __str__(self):
        return f"{self.gym.name} - {self.class_type.name} - {self.starts_at}"