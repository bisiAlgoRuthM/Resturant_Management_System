from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View #import generic view clas

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')