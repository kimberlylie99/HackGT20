# from django.shortcuts import render
from django.views import generic
from .forms import TOSInputForm

class IndexView(generic.FormView):
    template_name = 'text_input/index.html'
    form_class = TOSInputForm