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
    path('loadResume/', views.loadResume, name='loadResume'),
    path('quickResume/<int:user_id>', views.quickResume, name='quickResume'),
    path('add_Skill/', views.add_Skill, name='add_Skill'),
    path('add_Job/', views.add_Job, name='add_Job'),
    path('add_Education/', views.add_Education, name='add_Education'),
    ]
#comment so I can re-push
