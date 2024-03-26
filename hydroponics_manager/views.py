from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import HydroponicSystemForm
from .models import HydroponicSystem


# CRUD HydroponicSystem Views
class HydroponicSystemCreateView(LoginRequiredMixin, CreateView):
    model = HydroponicSystem
    template_name = "hydroponics_system/form.html"
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
    template_name = "hydroponics_system/detail.html"


class HydroponicSystemUpdateView(LoginRequiredMixin, CustomPassesTestMixin, UpdateView):
    model = HydroponicSystem
    template_name = "hydroponics_system/form.html"
    form_class = HydroponicSystemForm
    extra_context = {"button_name": "Update"}


class HydroponicSystemDeleteView(LoginRequiredMixin, CustomPassesTestMixin, DeleteView):
    model = HydroponicSystem
    template_name = "hydroponics_system/delete_confirm.html"
    success_url = reverse_lazy("hydroponic_system:list")


class HydroponicSystemListView(LoginRequiredMixin, ListView):
    model = HydroponicSystem
    template_name = "hydroponics_system/list.html"

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)
