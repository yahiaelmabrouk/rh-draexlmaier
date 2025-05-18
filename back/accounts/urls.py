from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home.html', views.home),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('managers/', views.manager_list, name='manager_list'),
    path('managers/add/', views.manager_add, name='manager_add'),
    path('managers/<int:pk>/edit/', views.manager_edit, name='manager_edit'),
    path('managers/<int:pk>/delete/', views.manager_delete, name='manager_delete'),
    path('welcome/', views.manager_welcome, name='manager_welcome'),
    path('about/', views.about, name='about'),
    path('data/', views.data, name='data'),
    path('accounts/', views.manager_list, name='account_list'),
    path('dashboards/', views.dashboards, name='dashboards'),  # <-- fix: use dashboards view
    path('manager/change-password/', views.manager_change_password, name='manager_change_password'),
]
