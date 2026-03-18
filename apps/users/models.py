# User models for the investment tracking system
# Currently using Django's built-in User model

from django.contrib.auth.models import AbstractUser
from django.db import models


# For now, we use Django's default User model
# Future extensions can be added here if needed

class UserProfile(models.Model):
    """Extended user profile for investment preferences"""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    risk_tolerance = models.CharField(
        max_length=20, 
        choices=[
            ('conservative', '保守型'),
            ('moderate', '稳健型'),
            ('aggressive', '激进型')
        ],
        default='moderate'
    )
    default_currency = models.CharField(max_length=3, default='CNY')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "用户配置"
        verbose_name_plural = "用户配置列表"
    
    def __str__(self):
        return f"{self.user.username} - {self.risk_tolerance}"
