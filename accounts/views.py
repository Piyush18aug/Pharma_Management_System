from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        if self.request.user.role == 'ADMIN':
            return reverse_lazy('inventory:admin_dashboard')
        return reverse_lazy('inventory:dashboard') 

class CustomLogoutView(LogoutView):
    next_page = 'login'
