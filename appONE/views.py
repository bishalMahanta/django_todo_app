from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import TasksTable
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

# built-in login view import
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


# login
class CustomLoginView(LoginView):
    template_name = "appONE/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy("tasks-list")


# user signup
class RegisterPage(CreateView):
    template_name = "appONE/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("tasks-list")
        return super(RegisterPage, self).get(*args, **kwargs)


# view tasks
class TasksView(LoginRequiredMixin, ListView):
    model = TasksTable
    context_object_name = "tasks"

    # user can see their task only:
    # override get_context_data() method to pass more information to context,
    # context is a dictionary (remember from function base view).
    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )  # getting orginal context dictionary
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(completed=False).count()

        # search functionality:
        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["tasks"] = context["tasks"].filter(title__icontains=search_input)

        context["search_input"] = search_input

        return context


# create tasks
class TasksCreate(LoginRequiredMixin, CreateView):
    model = TasksTable
    fields = ["title", "description", "completed"]
    success_url = reverse_lazy("tasks-list")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # The default implementation for form_valid() simply redirects to the success_url.
        form.instance.user = self.request.user
        return super(TasksCreate, self).form_valid(form)


# update task
class TasksEdit(LoginRequiredMixin, UpdateView):
    model = TasksTable
    fields = ["title", "description", "completed"]
    success_url = reverse_lazy("tasks-list")


# Delete task
class TasksDelte(LoginRequiredMixin, DeleteView):
    model = TasksTable
    context_object_name = "task"
    template_name = "appONE/delete.html"
    success_url = reverse_lazy("tasks-list")


# 404 page handle, not defined urls, redirect to tasks page.
def error_404(request, exception):
    # return render(request, "appONE/taskstable_list.html")
    # return HttpResponse("no page!")
    return HttpResponseRedirect(reverse("tasks-list"))
