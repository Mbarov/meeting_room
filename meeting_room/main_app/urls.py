from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('new_booking', views.new_booking, name='new_booking'),
    path('index/<int:event_id>', views.event_detail, name='event_detail'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('remove/<int:event_id>', views.event_remove, name='remove'),
    path('calendar/<int:year>/<int:week_number>/', views.calendar, name='calendar'),
    path('another/<str:action>/<int:year>/<int:week_number>', views.another_week, name='another_week'),
]
