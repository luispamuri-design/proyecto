from django.db import models
from django.contrib.auth.models import AbstractUser
#esto es de la base de datos



class Tipo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
 
    def __str__(self):
        return self.nombre
   
class User(AbstractUser):
    # Aquí ya no importamos Tipo directamente
    tipo = models.ForeignKey('proyecto.Tipo', on_delete=models.SET_NULL, null=True, blank=True)  
 
    def __str__(self):
        return f"{self.username} - {self.tipo.nombre if self.tipo else 'Sin rol'}"


class Service(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Veterinarian(models.Model):
    name = models.CharField(max_length=120)
    specialty = models.CharField(max_length=120, blank=True)
    shift = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    owner_name = models.CharField(max_length=150)
    pet_name = models.CharField(max_length=150)
    pet_type = models.CharField(max_length=50)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField()
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner_name} - {self.pet_name} ({self.date_time})"
   
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def __str__(self):
        return self.title