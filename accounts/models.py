from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    user_type = models.CharField(max_length=20, )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.user.first_name} {self.user.last_name}"


def user_avatar_path(instance, filename):
    return f'avatars/{instance.user.username}/{filename}'


def user_certificate_path(instance, filename):
    return f'certificates/{instance.user.username}/{filename}'


class Freelancer(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    certificate_id = models.CharField(max_length=100)
    certificate_expiration = models.DateField(blank=True, null=True)
    certificate_image = models.ImageField(upload_to=user_certificate_path)
    avatar = models.ImageField(upload_to=user_avatar_path)
    internal_rating = models.FloatField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} | {self.status}"

    def get_completion_count(self):
        completion_count = self.offer_set.filter(stage='Completed').count()
        return completion_count

    def get_cancellation_count(self):
        cancellation_count = self.offer_set.filter(stage='Cancelled').count()
        return cancellation_count

    def get_completion_rate(self):
        if self.offer_set.count() == 0:
            return 1
        else:
            completion_rate = self.get_completion_count() / (
                    self.get_completion_count() + self.get_cancellation_count())
            return completion_rate

    def get_timely_completion_count(self):
        timely_completion_count = self.offer_set.filter(stage='Completed', complete_on_time=True).count()
        return timely_completion_count

    def get_success_rate(self):
        if self.offer_set.count() == 0:
            return 1
        else:
            success_rate = self.get_timely_completion_count() / self.get_completion_count()
            return success_rate

    def get_freelancer_rating(self):
        pass

    def update_internal_rating(self):
        self.internal_rating = 0.3 * self.get_completion_rate() + 0.4 * self.get_success_rate() + 0.3 * self.get_freelancer_rating()
