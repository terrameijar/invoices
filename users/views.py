from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from .forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully")
        return super().form_valid(form)
