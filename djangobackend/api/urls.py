from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    # REST endpoints (RMM Level 1/2) 
    path('todos/', views.todo_list, name='todo-list'),
    path('todos/<int:id>/', views.todo_detail, name='todo-detail'),
    
    # Legacy POX endpoints (RMM Level 0) 
    path('todos/gettodos/', views.gettodos_pox, name='gettodos'),
    path('todos/getTodoById/', views.getTodoById_pox, name='getTodoById'),
    path('todos/createTodo/', views.createTodo_pox, name='createTodo'),

    path('hello/', views.test_hello, name='test_hello')
]