from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views import generic
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm
from agents.mixins import OrganisorAndLoginRequiredMixin

class SignupView(generic.CreateView):
  template_name = "registration/signup.html"
  form_class = CustomUserCreationForm

  def get_success_url(self):
    return reverse("login")


class LandingPageView(generic.TemplateView):
  template_name = "landing.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
  template_name = "leads/lead_list.html"
  context_object_name = "leads"

  def get_queryset(self):
    user = self.request.user

    # initial queryset of leads for the entire organisation
    if user.is_organisor:
      queryset = Lead.objects.filter(organisation=user.userprofile)
    else:
      queryset = Lead.objects.filter(organisation=user.agent.organisation)
      # filter for the current agent (logged in)
      queryset = queryset.filter(agent__user=user)
    return queryset


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = "leads/lead_detail.html"
  context_object_name = "lead"

    def get_queryset(self):
      user = self.request.user

      # initial queryset of leads for the entire organisation
      if user.is_organisor:
        queryset = Lead.objects.filter(organisation=user.userprofile)
      else:
        queryset = Lead.objects.filter(organisation=user.agent.organisation)
        # filter for the current agent (logged in)
        queryset = queryset.filter(agent__user=user)
      return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
  template_name = "leads/lead_create.html"
  form_class = LeadModelForm

  def get_success_url(self):
    return reverse("leads:lead-list")

  def form_valid(self, form):
    send_mail(
      subject="A lead has been created",
      message="Go to the site to see the new lead!",
      from_email="test@test.com",
      recipient_list=["test2@test.com"]
    )
    return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
  template_name = "leads/lead_update.html"
  form_class = LeadModelForm

  def get_queryset(self):
    user = self.request.user
    return Lead.objects.filter(organisation=user.userprofile)

  def get_success_url(self):
    return reverse("leads:lead-detail")


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
  template_name = "leads/lead_delete.html"

  def get_queryset(self):
    user = self.request.user
    return Lead.objects.filter(organisation=user.userprofile)

  def get_success_url(self):
    return reverse("leads:lead-list")

