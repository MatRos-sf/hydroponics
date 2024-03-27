from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .forms import CustomCreateUserForm, HydroponicSystemForm
from .models import HydroponicSystem


class SignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomCreateUserForm
    template_name = "hydroponics_manager/form.html"
    extra_context = {"button_name": "Sign Up"}
    success_url = reverse_lazy("hydroponic_system:login")
    success_message = "User was created successfully"


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("hydroponic_system:login")


# CRUD HydroponicSystem Views
class HydroponicSystemCreateView(LoginRequiredMixin, CreateView):
    model = HydroponicSystem
    template_name = "hydroponics_manager/form.html"
    form_class = HydroponicSystemForm
    extra_context = {"button_name": "Create"}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return super(HydroponicSystemCreateView, self).form_valid(form)


class CustomPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return HydroponicSystem.objects.filter(
            owner=self.request.user, pk=self.kwargs.get("pk")
        ).exists()


class HydroponicSystemDetailView(LoginRequiredMixin, CustomPassesTestMixin, DetailView):
    model = HydroponicSystem
    template_name = "hydroponics_manager/detail.html"


class HydroponicSystemUpdateView(LoginRequiredMixin, CustomPassesTestMixin, UpdateView):
    model = HydroponicSystem
    template_name = "hydroponics_manager/form.html"
    form_class = HydroponicSystemForm
    extra_context = {"button_name": "Update"}


class HydroponicSystemDeleteView(LoginRequiredMixin, CustomPassesTestMixin, DeleteView):
    model = HydroponicSystem
    template_name = "hydroponics_manager/delete_confirm.html"
    success_url = reverse_lazy("hydroponic_system:list")


class HydroponicSystemListView(LoginRequiredMixin, ListView):
    model = HydroponicSystem
    template_name = "hydroponics_manager/list.html"

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)
