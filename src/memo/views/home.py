from django.views import View
from django.shortcuts import render, redirect, get_object_or_404


class HomePage(View):
    def get(self, request, *args, **kwargs):
        """Render home page. Anonymous see login, register buttons. Logged in user see logout and profile buttons"""
        return render(request, 'home.html', {})
