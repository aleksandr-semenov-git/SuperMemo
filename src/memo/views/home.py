from django.views import View
from django.shortcuts import render, redirect, get_object_or_404


class HomePage(View):
    def get(self, request, *args, **kwargs):
        """"""
        return render(request, 'home.html', {})
