from django.urls import path
from . import views

urlpatterns = [
    path('', views.destination_list, name='destination_list'),
    path('add-destination/', views.add_destination, name='add_destination'),
    path('<int:destination_id>/add-expense/', views.add_expense, name='add_expense'),
    path('<int:destination_id>/expenses/', views.expense_list, name='expense_list'),
]
