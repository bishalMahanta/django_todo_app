from django.urls import path
from .views import (
    TasksView,
    TasksCreate,
    TasksEdit,
    TasksDelte,
    CustomLoginView,
    RegisterPage,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", RegisterPage.as_view(), name="signup"),
    path("", TasksView.as_view(), name="tasks-list"),
    path("task-create/", TasksCreate.as_view(), name="task-create"),
    path("task-edit/<int:pk>/", TasksEdit.as_view(), name="task-edit"),
    path("task-delete/<int:pk>/", TasksDelte.as_view(), name="task-delete"),
]
