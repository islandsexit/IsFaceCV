from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkin', views.auth, name='auth')
    # path('created/', views.added, name='created')
]
