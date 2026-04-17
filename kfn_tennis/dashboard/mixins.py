from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy


class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("dashboard:login")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет доступа к этой странице.")
        return super().handle_no_permission()