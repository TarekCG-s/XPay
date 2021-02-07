from django.contrib import admin
from django.urls import path
from .views import AnswersViewset

urlpatterns = [
    path('answers/', AnswersViewset.as_view(), name='answers'),
]
