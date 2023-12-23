from django.urls import path
from . import views
import logging

logger = logging.getLogger('url_logger')
handler404 = views.custom_404
handler500 = views.custom_500
urlpatterns=[
    path('',views.index, name='index'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_login', views.user_login, name='user_login'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('user_registration/',views.user_registration, name='user_registration'),
    path('user_registration',views.user_registration, name='user_registration'),
    path('user_home/',views.user_home, name='user_home'),
    path('user_report_incident/',views.user_report_incident, name='user_report_incident'),
    path('user_check_status/',views.user_check_status, name='user_check_status'),
    path('user_check_crime_rate/',views.user_check_crime_rate, name='user_check_crime_rate'),
    #path('user_crime_rate_result/',views.user_crime_rate_result, name='user_crime_rate_result'),
    path('officer_login/',views.officer_login, name='officer_login'),
    path('officer_home/',views.officer_home, name='officer_home'),
    path('update_status/', views.update_status, name='update_status'),
    path('send_emergency_alert/', views.send_emergency_alert, name='send_emergency_alert'),
    #path('officer_home/updatestatus/', views.update_status, name='update_status'),
    path('logout/',views.logout,name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('enter_otp/', views.enter_otp, name='enter_otp'),
    path('change_password/', views.change_password, name='change_password')

    
    

]

for pattern in urlpatterns:
    if hasattr(pattern, 'callback') and callable(pattern.callback):
        view_func = pattern.callback
        logger.info(f"Registered URL pattern: {pattern.pattern} - View: {view_func.__module__}.{view_func.__name__}")