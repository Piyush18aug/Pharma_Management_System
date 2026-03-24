from django import forms
from .models import Medicine, Category

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'batch_number', 'category', 'quantity', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
