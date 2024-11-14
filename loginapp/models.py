from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
'''
class EmailVerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    @staticmethod
    def generate_code():
        return str(random.randint(1000, 9999))

    def is_expired(self):
        time_difference = timezone.now() - self.created_at
        return time_difference.total_seconds() > 300  # 5 minutes in seconds
'''

from django.db import models
from django.contrib.auth.models import User
import random

class EmailVerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    @staticmethod
    def generate_code():
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])

    def is_expired(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at + timedelta(minutes=5) < timezone.now()