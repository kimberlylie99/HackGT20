from django.urls import path

from . import views

app_name = 'text_input'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]