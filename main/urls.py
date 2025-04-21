from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calc', views.calc, name='calc'),
    path('calc_p_profile', views.calc_p_profile, name='calc_p_profile'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('registration', views.user_reg, name='reg'),
    path('profile', views.profile, name='profile'),
    path('delete_fertilizer/<int:pk>', views.delete_fertilizer, name='delete_fertilizer'),
    path('add_fertilizer', views.add_fertilizer, name='add_fertilizer'),
    path('edit_fertilizer/<int:pk>', views.edit_fertilizer, name='edit_fertilizer'),
    path('profile_pp', views.profile_pp, name='profile_pp'),
    path('delete_p_profile/<int:pk>', views.delete_p_profile, name='delete_p_profile'),
    path('add_p_profile', views.add_p_profile, name='add_p_profile'),
    path('edit_p_profile/<int:pk>', views.edit_p_profile, name='edit_p_profile'),
    path('upload_p_profiles', views.upload_p_profiles, name='upload_p_profiles'),
    path('download_p_profiles', views.download_p_profiles, name='download_p_profiles'),
    path('upload_fertilizers', views.upload_fertilizers, name='upload_fertilizers'),
    path('download_fertilizers', views.download_fertilizers, name='download_fertilizers'),
    path('download_p_profiles_example', views.download_p_profiles_example, name='download_p_profiles_example'),
    path('download_fertilizers_example', views.download_fertilizers_example, name='download_fertilizers_example'),
]