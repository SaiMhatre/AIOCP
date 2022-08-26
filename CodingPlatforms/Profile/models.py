from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    fn = models.CharField(max_length= 100, default='')
    ln = models.CharField(max_length=100, default='')
    gh = models.CharField(max_length=100, default='')
    LinkedIn = models.CharField(max_length=100, default='')
    cf = models.CharField(max_length=100, default='')
    cc = models.CharField(max_length=100, default='')
    sj = models.CharField(max_length=100, default='')
    lc = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username
# Create your models here.
