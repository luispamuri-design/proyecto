from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Tipo
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required 
from .models import Service, Veterinarian, Appointment
from .forms import AppointmentForm
from .models import BlogPost

User = get_user_model()
# Create your views here.

def vista_login(request):
    return render(request, 'Login/index.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Intentamos obtener el usuario
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
            messages.error(request, 'El usuario no existe.')

        if user:
            user_authenticated = authenticate(request, username=username, password=password)
            if user_authenticated is not None:
                if user_authenticated.is_active:
                    login(request, user_authenticated)
                    return redirect('home')
                else:
                    messages.error(request, 'Tu cuenta de usuario está inactiva.')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'Login/index.html')



def register_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe.')
            return redirect('register_cliente')

        # Asegurarse de que exista el tipo 'cliente'
        tipo_cliente, created = Tipo.objects.get_or_create(nombre='cliente')

        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            first_name=nombre,
            last_name=apellido,
            password=password,
            tipo=tipo_cliente
        )

        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('custom_login')

    # Si es GET, mostramos el formulario
    return render(request, 'usuario/register_cliente.html')


@login_required(login_url='custom_login')
def home(request):
    return render(request, 'home/index.html', {'usuario': request.user})


def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    response = redirect('custom_login')  # Redirige a la página de login
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Evita que el navegador almacene caché
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required(login_url='custom_login')
def vista_usuario(request):
    roles = Tipo.objects.exclude(nombre__in=['root','cliente'])
    return render(request, 'usuario/index.html', {'usuario': request.user, 'roles': roles})

def home_cliente(request):
    services = Service.objects.all()
    doctors = Veterinarian.objects.all()[:5]
    posts = []  # luego puedes poblar desde un modelo Blog
    return render(request, 'home_cliente.html', {'services': services, 'doctors': doctors, 'posts': posts})

def services_list(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def doctors_list(request):
    doctors = Veterinarian.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors})

def contact(request):
    return render(request, 'contact.html')

def book_appointment(request):
    # si viene ?service=id preselecciona
    initial = {}
    service_id = request.GET.get('service')
    if service_id:
        initial['service'] = service_id

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            # opcional: enviar correo o crear link WhatsApp para confirmación
            messages.success(request, 'Cita creada. Revisa tu email o WhatsApp para confirmar.')
            return redirect('home_cliente')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AppointmentForm(initial=initial)
    return render(request, 'book_appointment.html', {'form': form})

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')  # Los más recientes primero
    return render(request, 'blog/blog_list.html', {'posts': posts})

def agendar_cita(request):
    # Lógica para agendar la cita
    return render(request, 'agendar_cita.html')

def home_cliente(request):
    return render(request, 'home/home_cliente.html')