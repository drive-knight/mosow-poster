from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page, name='page'),
    path('poster/<slug:slug>', views.place_detail, name='place'),
]