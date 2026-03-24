from django.utils import timezone
from datetime import timedelta
from .models import Medicine, ExpiryAlert

def check_and_create_alerts():
    """
    Checks for medicines near expiry or expired and creates alerts.
    Default threshold is 30 days.
    """
    threshold_days = 30 # Could be dynamic setting
    today = timezone.now().date()
    limit_date = today + timedelta(days=threshold_days)
    
    # Find medicines expiring soon or expired
    # Expiring Soon: between today and limit_date
    # Expired: < today
    
    medicines = Medicine.objects.filter(expiry_date__lte=limit_date)
    
    count = 0
    for med in medicines:
        # Check if ANY alert exists for this medicine (resolved or unresolved)
        if ExpiryAlert.objects.filter(medicine=med).exists():
            continue

        # Create new alert if none exists
        ExpiryAlert.objects.create(
            medicine=med,
            is_resolved=False,
            date_detected=today
        )
        count += 1
            
    return count
