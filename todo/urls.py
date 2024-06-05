from django.urls import path
from todo.views import *

app_name = 'todo'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create_task/', CreateTask.as_view(), name='create_task'),
    path('completed_task/<int:pk>/', CompletedTask.as_view(), name='completed_task'),
    path('edit_task/<int:pk>/', EditTask.as_view(), name='edit_task'),
    path('delete_task/<int:pk>/', DeleteTask.as_view(), name='delete_task'),
    path('get_task/<int:pk>/', GetTask.as_view(), name='get_task'),
    path('search_task/', SearchTask.as_view(), name='search_task')
]
