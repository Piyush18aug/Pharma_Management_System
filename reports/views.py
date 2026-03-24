import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from inventory.models import Medicine

@login_required
def export_inventory_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Batch', 'Category', 'Quantity', 'Expiry Date'])

    medicines = Medicine.objects.all().select_related('category')
    for med in medicines:
        writer.writerow([med.name, med.batch_number, med.category.name, med.quantity, med.expiry_date])

    return response

@login_required
def export_expired_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expired_medicines_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Batch', 'Category', 'Quantity', 'Expiry Date'])

    today = timezone.now().date()
    medicines = Medicine.objects.filter(expiry_date__lt=today).select_related('category')
    for med in medicines:
        writer.writerow([med.name, med.batch_number, med.category.name, med.quantity, med.expiry_date])

    return response
