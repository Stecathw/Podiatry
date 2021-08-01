from django.urls import path

from . import views

app_name = 'podologie'
urlpatterns = [
    path('', views.index, name='index'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
     
    path('rdv/', views.rdv, name='rdv'),
    path('mon_compte/', views.mon_compte, name='mon_compte'),
    
    # API for appointments
    path('api/available_ts/', views.available_ts, name='available_ts'),
    path('api/create_appointment/', views.create_appointment, name='create_appointment'),
    path('api/delete_appointment/', views.delete_appointment, name='delete_appointment'),
    
    # API for management
    path('api/get_unavailability/', views.get_unavailability, name='get_unavailability'),
    path('api/close_dates/', views.close_dates, name='close_dates'),
]