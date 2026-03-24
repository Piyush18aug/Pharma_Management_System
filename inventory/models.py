from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    batch_number = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    expiry_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_expired(self):
        return self.expiry_date < timezone.now().date()
        
    def days_until_expiry(self):
        delta = self.expiry_date - timezone.now().date()
        return delta.days
        
    def is_near_expiry(self, threshold_days=30):
        days = self.days_until_expiry()
        return 0 <= days <= threshold_days

    def __str__(self):
        return f"{self.name} - {self.batch_number}"

class ExpiryAlert(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    date_detected = models.DateField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Alert: {self.medicine.name} expiring on {self.medicine.expiry_date}"

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50) # CREATED, UPDATED, DELETED
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"
