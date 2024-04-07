from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editor/', views.editor, name='editor'),
    path('saveResume/', views.saveResume, name='saveResume'),
    path('makeResume/<int:user_id>', views.makeResume, name='makeResume')
    ]
#comment so I can re-push