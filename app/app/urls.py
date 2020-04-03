from django.urls import path

from greetings import views


urlpatterns = [
    path('greetings/', views.generate_greeting, name='generate'),
]
