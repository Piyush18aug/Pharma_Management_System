from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from .models import Medicine, Category, ExpiryAlert
from .forms import MedicineForm
from .utils import check_and_create_alerts

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Run alert check
        check_and_create_alerts()
        
        today = timezone.now().date()
        threshold_days = 30
        limit_date = today + timezone.timedelta(days=threshold_days)

        context['total_medicines'] = Medicine.objects.count()
        
        # Filter out medicines that have resolved alerts from the statistics
        # behaving like "Action Items" that need attention
        context['expired_medicines'] = Medicine.objects.filter(
            expiry_date__lt=today
        ).exclude(expiryalert__is_resolved=True).count()
        
        context['expiring_soon'] = Medicine.objects.filter(
            expiry_date__gte=today, 
            expiry_date__lte=limit_date
        ).exclude(expiryalert__is_resolved=True).count()
        
        # Get active alerts
        context['alerts'] = ExpiryAlert.objects.filter(is_resolved=False).select_related('medicine').order_by('medicine__expiry_date')
        
        return context

class AdminDashboardView(DashboardView):
    # Same as dashboard but might add more administrative context
    template_name = 'inventory/admin_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Very basic check, in reality use UserPassesTestMixin
        if not request.user.is_staff and not request.user.is_superuser:
             # Fallback or error
             return redirect('inventory:dashboard')
        return super().dispatch(request, *args, **kwargs)

class MedicineListView(LoginRequiredMixin, ListView):
    model = Medicine
    template_name = 'inventory/medicine_list.html'
    context_object_name = 'medicines'
    
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('search')
        cat_id = self.request.GET.get('category')
        
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(batch_number__icontains=query))
        
        if cat_id:
            qs = qs.filter(category_id=cat_id)
            
        return qs.order_by('expiry_date') # Default sort by expiry
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class MedicineCreateView(LoginRequiredMixin, CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'inventory/medicine_form.html'
    success_url = reverse_lazy('inventory:medicine_list')

class MedicineUpdateView(LoginRequiredMixin, UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'inventory/medicine_form.html'
    success_url = reverse_lazy('inventory:medicine_list')

class MedicineDeleteView(LoginRequiredMixin, DeleteView):
    model = Medicine
    template_name = 'inventory/medicine_confirm_delete.html'
    success_url = reverse_lazy('inventory:medicine_list')

def resolve_alert(request, pk):
    if not request.user.is_authenticated:
         return redirect('login')
    alert = get_object_or_404(ExpiryAlert, pk=pk)
    alert.is_resolved = True
    alert.resolved_at = timezone.now()
    alert.save()
    return redirect('inventory:dashboard')


