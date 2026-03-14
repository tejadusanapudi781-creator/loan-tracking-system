from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('add-borrower/', views.add_borrower, name='add_borrower'),
    path('add-collection/', views.add_collection, name='add_collection'),
]
