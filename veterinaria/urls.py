from django.contrib import admin
from proyecto import views 
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.vista_login),  # Nota: aquí apuntaba a vista_login
    path('loguearser', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='logout'),
    path('home', views.home, name='home'),
    path('register/', views.register_cliente, name='register_cliente'),
    path('vista_usuario', views.vista_usuario, name='vista_usuario'),
   # path('', views.custom_login, name='custom_login'),   # si quieres login en root
    path('home/', views.home_cliente, name='home_cliente'),
    path('services/', views.services_list, name='services'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('doctors/', views.doctors_list, name='doctors'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog_list'),  
    path('agendar_cita/', views.agendar_cita, name='agendar_cita'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

