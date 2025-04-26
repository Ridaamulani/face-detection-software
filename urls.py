from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from attendanceApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('register/', register, name="register"),
    path('signin/', signin, name="signin"),
    path('change-password/', change_password, name="change_password"),
    path('update-profile/', update_profile, name="update_profile"),
    path('logout-user/', logout_user, name="logout_user"),

    path('search-product/', search_product, name="search_product"),
    path('my-attendance/', my_attendance, name="my_attendance"),
    path('all-user/', all_user, name="all_user"),
    path('attendance-detail/<int:pid>/', attendance_detail, name="attendance_detail"),

    path('admin-signin/', admin_signin, name="admin_signin"),
    path('delete-user/<int:pid>/', delete_user, name="delete_user"),
    path('delete-attendance/<int:pid>/', delete_attendance, name="delete_attendance"),
    path('predict-data/', predict_data, name="predict_data"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
