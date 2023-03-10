from django.db import models
from django.contrib.auth.models import User
from setparam.models import UnitBoiler
from enum import Enum
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    class EmployeeStatus(models.TextChoises):
        OPERATOR = "OPERATOR"
        SUPERVISOR = "SUPERVISOR"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=EmployeeStatus.choices,
        default= EmployeeStatus.OPERATOR
    )
    unit = models.ForeignKey(UnitBoiler, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return "%s %s" %(self.first_name, self.last_name)


